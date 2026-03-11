#!/usr/bin/env python3
"""
ioctv24.com 直播流地址抓取工具 (Strict Logic Version)
逻辑说明:
    1. 默认模式 (不加 --all): 
       - 仅扫描正在直播的频道。
       - 仅保存【有有效播放地址】的频道到 JSON。
       - 没地址的、未开播的，直接丢弃，不写入文件。
    2. --all 模式:
       - 扫描所有频道。
       - 保存所有频道信息 (无论是否有地址)。

用法:
    python3 ioctv_grabber_strict.py              # 仅处理并保存可播放的直播
    python3 ioctv_grabber_strict.py --all        # 处理并保存所有频道 (含无地址的)
    python3 ioctv_grabber_strict.py --filter nba # 过滤并保存可播放的
"""

import re
import os
import sys
import time
import json
import argparse
import subprocess
import shutil
import logging
from typing import Optional, List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict

try:
    import requests
    from requests.exceptions import RequestException, Timeout
except ImportError:
    print("❌ 错误: 缺少依赖库 'requests'。请运行: pip3 install requests")
    sys.exit(1)

# ─── 配置 ───────────────────────────────────────────────

@dataclass
class Config:
    HOME_URL: str = "https://ioctv24.com/"
    BROADCAST_LIST_URL: str = "https://wdbroad.com/broadcast/ioctv"
    VIDEO_KEY_URL: str = "https://wdbroad.com/player/getVideoKey.php"
    BROADCAST_DETAIL_TMPL: str = "https://wdbroad.com/broadcast/{id}/ioctv"
    
    OUTPUT_JSON_FILE: str = "ioctv_streams.json"
    EMOJI_CACHE_FILE: str = "ioctv_category_emoji_cache.json"
    EMOJI_CACHE_TTL_SECONDS: int = 6 * 60 * 60
    REQUEST_TIMEOUT: int = 15
    MAX_WORKERS: int = 8
    
    HEADERS: Dict[str, str] = field(default_factory=lambda: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://ioctv24.com/",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    EMOJI_RULES: List[Tuple[str, List[str]]] = field(default_factory=lambda: [
        ("⚾", ["WBC", "MLB", "NPB", "KBO", "BASEBALL", "야구"]),
        ("🏀", ["NBA", "KBL", "NBL", "B리그", "B.LEAGUE", "농구"]),
        ("🏒", ["NHL", "KHL", "하키", "HOCKEY"]),
        ("⚽", ["D1", "D2", "EPL", "UCL", "SERIE", "LIGA", "BUNDES", "K리그", "J리그", "축구", "CHA SL", "WWCPE"]),
        ("🏐", ["KOVO", "V리그", "VOLLEY", "배구"]),
        ("🤾", ["H리그", "HANDBALL", "핸드볼"]),
        ("🎮", ["LPL", "LCK", "ESPORT", "E-SPORT", "게임"]),
        ("🏸", ["BWF", "BADMINTON", "배드민턴"]),
        ("📺", ["SPORTS CH", "SPORTS", "NEWS", "TV"]),
    ])

CFG = Config()

# ─── 日志 ───────────────────────────────────────────────
logger = logging.getLogger("ioctv_grabber")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# ─── 数据模型 ───────────────────────────────────────────────

@dataclass
class BroadcastInfo:
    id: str
    name: str
    time: str
    site: str
    league: str
    emoji: str
    is_live: bool
    stream_path: Optional[str] = None
    full_url: Optional[str] = None

# ─── 核心逻辑 ───────────────────────────────────────────────

def get_base_url(session: requests.Session) -> str:
    try:
        resp = session.get(CFG.VIDEO_KEY_URL, headers={
            **CFG.HEADERS,
            "Referer": "https://wdbroad.com/broadcast/38/ioctv",
            "X-Requested-With": "XMLHttpRequest",
        }, timeout=CFG.REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        base = data.get("wghsoftnet", "")
        if not base:
            raise RuntimeError("API 返回数据中缺少 'wghsoftnet' 字段")
        return base.rstrip('/')
    except Exception as e:
        logger.error(f"无法获取视频服务器地址: {e}")
        raise

def infer_emoji(text: str) -> str:
    if not text: return "🏆"
    t = text.upper()
    for emoji, keywords in CFG.EMOJI_RULES:
        if any(k.upper() in t for k in keywords): return emoji
    return "🏆"

def build_dynamic_emoji_map(session: requests.Session) -> Dict[str, str]:
    dynamic_map: Dict[str, str] = {}
    candidates = set()
    try:
        resp = session.get(CFG.BROADCAST_LIST_URL, headers=CFG.HEADERS, timeout=CFG.REQUEST_TIMEOUT)
        matches = re.findall(r'<td\s+class="catesub"\s*>([^<]+?)</td>', resp.text, re.IGNORECASE)
        candidates.update(m.strip() for m in matches if m.strip())
    except: pass
    
    try:
        resp = session.get(CFG.HOME_URL, headers=CFG.HEADERS, timeout=CFG.REQUEST_TIMEOUT)
        keywords = ["NBA", "KBL", "V리그", "KOVO", "MLB", "NPB", "KBO", "NHL", "KHL", "LPL", "BWF", "D1", "D2"]
        for kw in keywords:
            if kw in resp.text: candidates.add(kw)
    except: pass
    
    for key in candidates:
        if key: dynamic_map[key] = infer_emoji(key)
    return dynamic_map

def load_emoji_cache() -> Optional[Dict[str, str]]:
    if not os.path.exists(CFG.EMOJI_CACHE_FILE): return None
    try:
        with open(CFG.EMOJI_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if time.time() - float(data.get("generated_at", 0)) > CFG.EMOJI_CACHE_TTL_SECONDS:
            return None
        return {str(k): str(v) for k, v in data.get("mapping", {}).items()}
    except: return None

def save_emoji_cache(mapping: Dict[str, str]):
    if not mapping: return
    try:
        temp = CFG.EMOJI_CACHE_FILE + ".tmp"
        with open(temp, "w", encoding="utf-8") as f:
            json.dump({"generated_at": time.time(), "mapping": mapping}, f, ensure_ascii=False, indent=2)
        os.replace(temp, CFG.EMOJI_CACHE_FILE)
    except: pass

def get_category_emoji_map(session: requests.Session, refresh_cache: bool = False) -> Dict[str, str]:
    if not refresh_cache:
        cached = load_emoji_cache()
        if cached:
            logger.info(f"已加载 emoji 缓存 ({len(cached)} 条)")
            return cached
    
    logger.info("正在构建动态 emoji 映射...")
    dynamic_map = build_dynamic_emoji_map(session)
    if dynamic_map:
        save_emoji_cache(dynamic_map)
        return dynamic_map
    
    if os.path.exists(CFG.EMOJI_CACHE_FILE):
        try:
            with open(CFG.EMOJI_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("mapping"):
                logger.warning("使用过期缓存")
                return {str(k): str(v) for k, v in data["mapping"].items()}
        except: pass
    return {}

def parse_broadcast_list(session: requests.Session, category_emoji: Dict[str, str]) -> List[BroadcastInfo]:
    try:
        resp = session.get(CFG.BROADCAST_LIST_URL, headers=CFG.HEADERS, timeout=CFG.REQUEST_TIMEOUT)
        html = resp.text
    except Exception as e:
        logger.error(f"获取列表失败: {e}")
        return []

    pattern = r"load_video\s*\(\s*['\"]broadcast/(\d+)['\"]\s*,\s*['\"](\d+)['\"]\s*,\s*['\"]([^']*)['\"]\s*,\s*['\"]([^']*)['\"]\s*,\s*['\"]([^']*)['\"]\s*,\s*['\"]([^']*)['\"]\s*\)"
    matches = re.findall(pattern, html)
    
    status_pattern = r"<img\s+src=['\"]/player/img/(on|off)air1\.gif['\"]"
    statuses = re.findall(status_pattern, html)

    broadcasts = []
    bid_league_map = {}
    block_pattern = r'<tr[^>]*>.*?<td\s+class="catesub"[^>]*>\s*([^<]+?)\s*</td>.*?load_video\s*\(\s*[\'"]broadcast/(\d+)[\'"]'
    for league_name, bid in re.findall(block_pattern, html, re.DOTALL | re.IGNORECASE):
        bid_league_map[bid] = league_name.strip()

    for i, (bid, mode, name, time_str, site, icon) in enumerate(matches):
        is_live = (statuses[i] == "on") if i < len(statuses) else False
        
        league = bid_league_map.get(bid, "")
        if not league:
            if "SPORTS CH" in name: league = "SPORTS"
            elif "NEWS" in name: league = "NEWS"
        
        emoji = "🏆"
        for k, v in category_emoji.items():
            if k in league or k in name:
                emoji = v
                break
        if emoji == "🏆": emoji = infer_emoji(f"{league} {name}")

        broadcasts.append(BroadcastInfo(
            id=bid,
            name=name.replace("&nbsp;", " ").strip().replace("\\'", "'"),
            time=time_str.replace("&nbsp;", " ").strip(),
            site=site,
            league=league,
            emoji=emoji,
            is_live=is_live
        ))
    return broadcasts

def fetch_stream_path(session: requests.Session, bid: str) -> Optional[str]:
    url = CFG.BROADCAST_DETAIL_TMPL.format(id=bid)
    try:
        resp = session.get(url, headers={
            **CFG.HEADERS,
            "Referer": "https://wdbroad.com/broadcast/ioctv",
        }, timeout=CFG.REQUEST_TIMEOUT)
        resp.raise_for_status()
        content = resp.text

        pattern_strict = r'data\.wghsoftnet\s*\+\s*["\']([^"\']+\.m3u8[^"\']*)["\']'
        match = re.search(pattern_strict, content)
        
        raw_path = None
        if match:
            raw_path = match.group(1)
        else:
            pattern_backup = r'["\'](/[^"\']*\.m3u8\?hmac=[^"\']*)["\']'
            match_backup = re.search(pattern_backup, content)
            if match_backup:
                raw_path = match_backup.group(1)

        if not raw_path:
            return None

        clean_path = raw_path.strip().rstrip('",\';')
        if ".m3u8" not in clean_path or "hmac=" not in clean_path:
            return None
            
        if not clean_path.startswith("http") and not clean_path.startswith("/"):
            clean_path = "/" + clean_path

        return clean_path
    except Exception:
        return None

def enrich_and_filter_streams(session: requests.Session, broadcasts: List[BroadcastInfo], 
                              base_url: str, fetch_all: bool = False, max_workers: int = 8) -> List[BroadcastInfo]:
    """
    fetch_all = False (默认):
      1. 只检查 is_live=True 的频道。
      2. 只返回那些成功获取到 full_url 的频道 (过滤掉无地址的)。
    
    fetch_all = True (--all):
      1. 检查所有频道。
      2. 返回所有频道对象 (无论是否有地址)。
    """
    
    if fetch_all:
        targets = broadcasts
        logger.info(f"模式 [--all]: 正在处理所有 {len(targets)} 个频道...")
        return_all = True
    else:
        # 默认模式：只关注直播中的
        targets = [b for b in broadcasts if b.is_live]
        logger.info(f"模式 [默认]: 正在处理 {len(targets)} 个正在直播的频道...")
        return_all = False

    if not targets:
        return []

    bid_map = {b.id: b for b in broadcasts} # 用于更新原始对象
    success_count = 0

    def _task(b: BroadcastInfo):
        return b.id, fetch_stream_path(session, b.id)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_task, b): b for b in targets}
        for future in as_completed(futures):
            try:
                bid, path = future.result()
                if bid in bid_map:
                    obj = bid_map[bid]
                    if path:
                        obj.stream_path = path
                        obj.full_url = path if path.startswith("http") else f"{base_url}{path}"
                        success_count += 1
                    # 如果 path 为 None，obj.full_url 保持 None
            except Exception as e:
                logger.debug(f"线程任务出错: {e}")

    logger.info(f"流地址获取完成: 成功 {success_count}/{len(targets)} 个")

    # 【关键逻辑】根据模式决定返回什么
    if return_all:
        # --all 模式：返回所有原始对象 (包含 url=None 的)
        return broadcasts
    else:
        # 默认模式：只返回有 url 的对象 (过滤掉无地址的)
        valid_broadcasts = [b for b in targets if b.full_url is not None]
        logger.info(f"过滤后剩余 {len(valid_broadcasts)} 个可播放频道")
        return valid_broadcasts

# ─── 保存逻辑 ───────────────────────────────────────────────

def auto_save(broadcasts: List[BroadcastInfo], filepath: str):
    """保存传入的列表到 JSON"""
    if not broadcasts:
        logger.warning("没有数据可保存 (列表为空)")
        # 即使为空也创建一个空文件或者不创建，这里选择不创建或创建空列表
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        logger.info(f"已创建空文件: {filepath}")
        return

    records = []
    for b in broadcasts:
        d = asdict(b)
        url_val = d.pop('full_url', None)
        d['url'] = url_val
        # 可选：移除内部路径字段以保持 JSON 干净
        d.pop('stream_path', None)
        records.append(d)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
            f.write("\n")
        
        has_url = sum(1 for r in records if r['url'])
        logger.info(f"✅ 数据已自动保存至: {filepath}")
        logger.info(f"   📊 共保存 {len(records)} 条记录 (其中 {has_url} 条有播放地址)")
        
    except IOError as e:
        logger.error(f"❌ 保存文件失败: {e}")

# ─── 输出与播放 ───────────────────────────────────────────────

def print_table(broadcasts: List[BroadcastInfo]):
    if not broadcasts:
        print("😴 没有找到可播放的直播流")
        return

    print()
    print(f"{'#':>3}  {'状态':<4} {'时间':<12} {'联赛':<10} {'比赛':<35}")
    print("-" * 70)

    for i, b in enumerate(broadcasts, 1):
        status = "🔴" if b.is_live else "⚫"
        league = f"{b.emoji} {b.league[:9]}" if b.league else f"{b.emoji} ?"
        print(f"{i:>3}  {status:<4} {b.time:<12} {league:<10} {b.name[:35]}")

        if b.full_url:
            print(f"       ▸ {b.full_url}")
        print()

    print(f"✅ 共列出 {len(broadcasts)} 个可播放频道")
    print(f"💾 已自动保存至: {CFG.OUTPUT_JSON_FILE}")
    print()

def output_json(broadcasts: List[BroadcastInfo]):
    records = []
    for b in broadcasts:
        d = asdict(b)
        d['url'] = d.pop('full_url', None)
        d.pop('stream_path', None)
        records.append(d)
    print(json.dumps(records, ensure_ascii=False, indent=2))

def generate_m3u(broadcasts: List[BroadcastInfo], filepath: str):
    items = [b for b in broadcasts if b.full_url]
    if not items:
        logger.warning("无可用直播流生成 M3U")
        return

    lines = ["#EXTM3U"]
    for b in items:
        safe_name = b.name.replace(",", "-").replace('"', "'")
        safe_league = b.league.replace(",", "-").replace('"', "'")
        lines.append(f'#EXTINF:-1 group-title="{safe_league}",{b.emoji} {safe_name} ({b.time})')
        lines.append(b.full_url)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        logger.info(f"✅ M3U 播放列表已生成: {filepath} ({len(items)} 个频道)")
    except IOError as e:
        logger.error(f"写入 M3U 失败: {e}")

def play_stream(broadcasts: List[BroadcastInfo], index: int):
    items = [b for b in broadcasts if b.full_url]
    if not items:
        logger.error("无可用直播流播放")
        return
    if index < 1 or index > len(items):
        logger.error(f"序号无效 (1-{len(items)})")
        return
    
    b = items[index-1]
    print(f"🎬 播放: {b.emoji} {b.name}")
    
    cmds = [
        ["iina", "--no-stdin", b.full_url],
        ["mpv", b.full_url],
        ["vlc", b.full_url],
        ["/Applications/IINA.app/Contents/MacOS/iina-cli", "--no-stdin", b.full_url]
    ]
    
    launched = False
    for cmd in cmds:
        exe = cmd[0]
        if shutil.which(exe) or (os.path.isabs(exe) and os.path.exists(exe)):
            try:
                logger.info(f"启动: {exe}")
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                launched = True
                break
            except: continue
    
    if not launched:
        if sys.platform == "darwin":
            subprocess.Popen(["open", b.full_url])
            launched = True
        else:
            logger.error("未找到播放器，请手动复制 URL")
            print(b.full_url)

# ─── 主入口 ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ioctv24 抓取工具 (严格逻辑版)")
    parser.add_argument("--all", action="store_true", help="获取并保存所有频道 (含无地址的)")
    parser.add_argument("--filter", "-f", type=str, help="过滤关键字")
    parser.add_argument("--play", "-p", type=int, help="播放第 N 个")
    parser.add_argument("--json", action="store_true", help="终端输出 JSON")
    parser.add_argument("--m3u", nargs="?", const="ioctv_live.m3u", metavar="FILE", help="生成 M3U")
    parser.add_argument("--refresh-emoji-cache", action="store_true", help="刷新缓存")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细日志")
    
    args = parser.parse_args()
    if args.verbose: logger.setLevel(logging.DEBUG)
    
    session = requests.Session()

    try:
        logger.debug("连接视频服务器...")
        base_url = get_base_url(session)
        
        logger.debug("获取赛事列表...")
        emoji_map = get_category_emoji_map(session, refresh_cache=args.refresh_emoji_cache)
        all_broadcasts = parse_broadcast_list(session, emoji_map)
        
        if not all_broadcasts:
            logger.error("未解析到任何比赛信息")
            sys.exit(1)

        # 过滤关键字 (在获取流之前先过滤，节省资源)
        if args.filter:
            kw = args.filter.lower()
            original_len = len(all_broadcasts)
            all_broadcasts = [b for b in all_broadcasts if kw in b.name.lower() or kw in b.league.lower() or kw in b.emoji]
            if not all_broadcasts:
                print(f"🔍 没有匹配 '{args.filter}' 的比赛")
                sys.exit(0)
            logger.info(f"过滤后剩余 {len(all_broadcasts)} 项待处理")

        # 【核心逻辑】获取流并决定是否过滤
        # fetch_all=args.all 控制行为：
        # False -> 只查直播，且只返回有 URL 的
        # True  -> 查所有，返回所有 (不管有无 URL)
        final_broadcasts = enrich_and_filter_streams(
            session, 
            all_broadcasts, 
            base_url, 
            fetch_all=args.all
        )

        # 【自动保存】保存的是经过上述逻辑处理后的 final_broadcasts
        # 默认模式下，这里只有有 URL 的频道
        # --all 模式下，这里有所有频道
        auto_save(final_broadcasts, CFG.OUTPUT_JSON_FILE)

        # 输出
        if args.json:
            output_json(final_broadcasts)
        elif args.m3u:
            generate_m3u(final_broadcasts, args.m3u)
        elif args.play is not None:
            print_table(final_broadcasts)
            play_stream(final_broadcasts, args.play)
        else:
            print_table(final_broadcasts)

    except KeyboardInterrupt:
        print("\n👋 已取消")
    except RequestException as e:
        logger.error(f"网络错误: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"未预期错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()