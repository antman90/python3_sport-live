#!/usr/bin/env python3
"""
ioctv24.com 直播流地址抓取工具
用法:
    python3 ioctv_grabber.py              # 列出所有正在直播的频道
    python3 ioctv_grabber.py --all        # 列出所有频道(含未开播)
    python3 ioctv_grabber.py --filter nba # 按关键字过滤
    python3 ioctv_grabber.py --play 1     # 用 IINA/mpv/VLC 播放第N个流
    python3 ioctv_grabber.py --json       # JSON 输出
    python3 ioctv_grabber.py --m3u        # 生成 M3U 播放列表文件
    python3 ioctv_grabber.py --save       # 保存流地址到文本文件
"""

import re
import os
import sys
import time
import json
import argparse
import subprocess
import shutil
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    print("❌ 需要 requests 库: pip3 install requests")
    sys.exit(1)


# ─── 配置 ───────────────────────────────────────────────
SITE_NAME = "ioctv"
HOME_URL = "https://ioctv24.com/"
BROADCAST_LIST_URL = "https://wdbroad.com/broadcast/ioctv"
VIDEO_KEY_URL = "https://wdbroad.com/player/getVideoKey.php"
BROADCAST_DETAIL_URL = "https://wdbroad.com/broadcast/{id}/ioctv"
EMOJI_CACHE_FILE = "ioctv_category_emoji_cache.json"
EMOJI_CACHE_TTL_SECONDS = 6 * 60 * 60

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://ioctv24.com/",
}

# 关键词规则（动态映射基础）
EMOJI_RULES = [
    ("⚾", ["WBC", "MLB", "NPB", "KBO", "BASEBALL", "야구"]),
    ("🏀", ["NBA", "KBL", "NBL", "B리그", "B.LEAGUE", "농구"]),
    ("🏒", ["NHL", "KHL", "하키", "HOCKEY"]),
    ("⚽", ["D1", "D2", "EPL", "UCL", "SERIE", "LIGA", "BUNDES", "K리그", "J리그", "축구", "CHA SL", "WWCPE"]),
    ("🏐", ["KOVO", "V리그", "VOLLEY", "배구"]),
    ("🤾", ["H리그", "HANDBALL", "핸드볼"]),
    ("🎮", ["LPL", "LCK", "ESPORT", "E-SPORT", "게임"]),
    ("🏸", ["BWF", "BADMINTON", "배드민턴"]),
    ("📺", ["SPORTS CH", "SPORTS", "NEWS", "TV"]),
]


# ─── 核心逻辑 ────────────────────────────────────────────

def get_base_url(session: requests.Session) -> str:
    """获取视频服务器基础 URL"""
    resp = session.get(VIDEO_KEY_URL, headers={
        **HEADERS,
        "Referer": "https://wdbroad.com/broadcast/38/ioctv",
        "X-Requested-With": "XMLHttpRequest",
    }, timeout=15)
    data = resp.json()
    base = data.get("wghsoftnet", "")
    if not base:
        raise RuntimeError("无法获取视频服务器地址")
    return base


def infer_emoji(text: str) -> str:
    """基于关键词推断 emoji"""
    t = (text or "").upper()
    for emoji, keywords in EMOJI_RULES:
        if any(k.upper() in t for k in keywords):
            return emoji
    return "🏆"


def build_dynamic_emoji_map(session: requests.Session) -> Dict[str, str]:
    """从 ioctv24 最近页面动态构建联赛->emoji 映射"""
    dynamic_map: Dict[str, str] = {}
    candidates = set()

    # 来源1: 直播列表页中的 catesub
    try:
        resp = session.get(BROADCAST_LIST_URL, headers=HEADERS, timeout=15)
        html = resp.text
        candidates.update(m.strip() for m in re.findall(r'<td class="catesub">\s*([^<]+?)\s*</td>', html))
    except Exception as e:
        print(f"  ⚠️ 动态分类来源1失败: {e}", file=sys.stderr)

    # 来源2: ioctv24 首页 최근 경기분석 标题（如 NBA/KBL/V리그）
    try:
        resp = session.get(HOME_URL, headers=HEADERS, timeout=15)
        home_html = resp.text
        candidates.update(m.strip() for m in re.findall(r"NBA|KBL|V리그|KOVO|MLB|NPB|KBO|NHL|KHL|LPL|BWF|KOR D1|JPN D1|JPN D2|GER D2|MEX D1|COL D1|AUS D1|CHA SL|UKR D1|WWCPE", home_html, flags=re.IGNORECASE))
    except Exception as e:
        print(f"  ⚠️ 动态分类来源2失败: {e}", file=sys.stderr)

    for key in candidates:
        if key:
            dynamic_map[key] = infer_emoji(key)

    return dynamic_map


def load_emoji_cache(filepath: str = EMOJI_CACHE_FILE,
                     ttl_seconds: int = EMOJI_CACHE_TTL_SECONDS) -> Optional[Dict[str, str]]:
    """读取缓存的联赛 emoji 映射（过期则返回 None）"""
    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        generated_at = float(data.get("generated_at", 0))
        mapping = data.get("mapping", {})
        if not isinstance(mapping, dict) or not mapping:
            return None
        if time.time() - generated_at > ttl_seconds:
            return None
        return {str(k): str(v) for k, v in mapping.items()}
    except Exception as e:
        print(f"  ⚠️ 读取 emoji 缓存失败: {e}", file=sys.stderr)
        return None


def save_emoji_cache(mapping: Dict[str, str], filepath: str = EMOJI_CACHE_FILE):
    """写入联赛 emoji 映射缓存"""
    if not mapping:
        return
    payload = {
        "generated_at": int(time.time()),
        "mapping": mapping,
    }
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  ⚠️ 写入 emoji 缓存失败: {e}", file=sys.stderr)


def get_category_emoji_map(session: requests.Session, refresh_cache: bool = False) -> Dict[str, str]:
    """优先读取缓存，按需刷新动态联赛 emoji 映射"""
    if not refresh_cache:
        cached = load_emoji_cache()
        if cached:
            print(f"🧠 已加载 emoji 缓存: {EMOJI_CACHE_FILE} ({len(cached)} 条)", file=sys.stderr)
            return cached

    dynamic_map = build_dynamic_emoji_map(session)
    if dynamic_map:
        save_emoji_cache(dynamic_map)
        print(f"♻️ 已刷新 emoji 缓存: {EMOJI_CACHE_FILE} ({len(dynamic_map)} 条)", file=sys.stderr)
        return dynamic_map

    # 动态获取失败时，回退到缓存（即使缓存过期也尽量可用）
    try:
        if os.path.exists(EMOJI_CACHE_FILE):
            with open(EMOJI_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            mapping = data.get("mapping", {})
            if isinstance(mapping, dict) and mapping:
                print("⚠️ 动态分类失败，使用旧缓存继续", file=sys.stderr)
                return {str(k): str(v) for k, v in mapping.items()}
    except Exception:
        pass

    return {}


def parse_broadcast_list(session: requests.Session, category_emoji: Optional[Dict[str, str]] = None) -> List[Dict]:
    """解析直播列表页，返回所有比赛信息"""
    resp = session.get(BROADCAST_LIST_URL, headers=HEADERS, timeout=15)
    html = resp.text

    # 提取比赛信息: load_video('broadcast/38', '1', '콜롬비아 vs 푸에르토리코', '03-07 08:00', 'ioctv', '/player/img/base.png')
    pattern = (
        r"load_video\('broadcast/(\d+)',\s*'1',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',"
        r"\s*'([^']*)'\);mode_1\(\);"
    )
    matches = re.findall(pattern, html)

    # 提取直播状态 (onair/offair)
    status_pattern = r"<img src='/player/img/(on|off)air1\.gif'"
    statuses = re.findall(status_pattern, html)

    broadcasts = []
    for i, (bid, name, time_str, site, icon) in enumerate(matches):
        is_live = statuses[i] == "on" if i < len(statuses) else False

        # 推断联赛/类别
        league = ""
        # 频道类
        if "SPORTS CH" in name:
            league = "SPORTS"
        elif "NEWS" in name:
            league = "NEWS"
        else:
            # 从页面上下文提取联赛 (catesub 在 subject 之前)
            league_pattern = (
                rf"<td class=\"catesub\">\s*([^<]+?)\s*</td>\s*"
                rf"<td class=\"subject\" onclick=\"load_video\('broadcast/{bid}'"
            )
            m = re.search(league_pattern, html)
            if m:
                league = m.group(1).strip()

        emoji = "🏆"
        for key, em in (category_emoji or {}).items():
            if key in league or key in name:
                emoji = em
                break
        if emoji == "🏆":
            emoji = infer_emoji(f"{league} {name}")

        # 清理 HTML 实体
        time_str = time_str.replace("&nbsp;", " ").strip()
        name = name.replace("&nbsp;", " ").strip()

        broadcasts.append({
            "id": bid,
            "name": name,
            "time": time_str,
            "site": site,
            "league": league,
            "emoji": emoji,
            "is_live": is_live,
            "stream_path": None,
            "full_url": None,
        })

    return broadcasts


def fetch_stream_path(session: requests.Session, bid: str) -> Optional[str]:
    """获取单个比赛的流路径（含 HMAC）"""
    url = BROADCAST_DETAIL_URL.format(id=bid)
    try:
        resp = session.get(url, headers={
            **HEADERS,
            "Referer": "https://wdbroad.com/broadcast/ioctv",
        }, timeout=15)
        # 提取: data.wghsoftnet + "live4/playlist.m3u8?hmac=...&site=ioctv&ch=live4"
        m = re.search(r'data\.wghsoftnet \+ "([^"]+)"', resp.text)
        if m:
            path = m.group(1).rstrip('",')
            return path
    except Exception as e:
        print(f"  ⚠️ broadcast/{bid} 获取失败: {e}", file=sys.stderr)
    return None


def enrich_streams(session: requests.Session, broadcasts: List[Dict], base_url: str,
                   live_only: bool = True, max_workers: int = 8) -> List[Dict]:
    """并发获取所有直播流的完整地址"""
    targets = [b for b in broadcasts if (not live_only or b["is_live"])]

    if not targets:
        return broadcasts

    print(f"🔍 正在获取 {len(targets)} 个频道的流地址...", file=sys.stderr)

    def _fetch(b):
        path = fetch_stream_path(session, b["id"])
        return b["id"], path

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_fetch, b): b for b in targets}
        for future in as_completed(futures):
            bid, path = future.result()
            for b in broadcasts:
                if b["id"] == bid and path:
                    b["stream_path"] = path
                    b["full_url"] = base_url + path
                    break

    return broadcasts


# ─── 输出格式 ────────────────────────────────────────────

def print_table(broadcasts: List[Dict], live_only: bool = True):
    """美化表格输出"""
    items = [b for b in broadcasts if (not live_only or b["is_live"])]
    if not items:
        print("😴 当前没有正在直播的频道")
        return

    print()
    print(f"  {'#':>3}  状态  {'时间':<12} {'联赛':<10} {'比赛':<40}")
    print(f"  {'─'*3}  ──  {'─'*12} {'─'*10} {'─'*40}")

    for i, b in enumerate(items, 1):
        status = "🔴" if b["is_live"] else "⚫"
        line = f"  {i:>3}  {status}  {b['time']:<12} {b['emoji']}{b['league']:<9} {b['name']:<40}"
        print(line)

        if b["full_url"]:
            print(f"       ▸ {b['full_url']}")
        elif b["is_live"]:
            print(f"       ▸ (流地址获取失败)")
        print()

    live_count = sum(1 for b in items if b["is_live"] and b["full_url"])
    print(f"  ✅ 共 {live_count} 个可用直播流")
    print(f"  💡 复制地址到 IINA / VLC / mpv 即可播放")
    print(f"  💡 或使用 --play N 直接播放第 N 个")
    print()


def output_json(broadcasts: List[Dict], live_only: bool = True):
    """JSON 输出"""
    items = [b for b in broadcasts if (not live_only or b["is_live"]) and b["full_url"]]
    print(json.dumps(items, ensure_ascii=False, indent=2))


def output_m3u(broadcasts: List[Dict], filepath: str = "ioctv_live.m3u"):
    """生成 M3U 播放列表"""
    items = [b for b in broadcasts if b["is_live"] and b["full_url"]]
    if not items:
        print("😴 没有可用的直播流")
        return

    lines = ["#EXTM3U"]
    for b in items:
        lines.append(f'#EXTINF:-1 group-title="{b["league"]}",{b["emoji"]} {b["name"]} ({b["time"]})')
        lines.append(b["full_url"])

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✅ 已生成播放列表: {filepath} ({len(items)} 个频道)")
    print(f"💡 用 VLC/IINA 打开这个文件即可")


def save_stream_urls(broadcasts: List[Dict], filepath: str,
                     live_only: bool = True):
    """保存流地址到 JSON 文件（含比赛信息）"""
    items = [b for b in broadcasts if (not live_only or b["is_live"]) and b["full_url"]]
    if not items:
        print(f"⚠️ 没有可保存的流地址: {filepath}")
        return

    # 去重并保持出现顺序（按 URL 去重）
    seen = set()
    records = []
    for b in items:
        url = b["full_url"]
        if url not in seen:
            seen.add(url)
            records.append({
                "id": b["id"],
                "time": b["time"],
                "league": b["league"],
                "emoji": b["emoji"],
                "name": b["name"],
                "site": b["site"],
                "is_live": b["is_live"],
                "url": url,
            })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"✅ 已保存 JSON 流地址: {filepath} ({len(records)} 条)")


def play_stream(broadcasts: List[Dict], index: int):
    """用本地播放器播放指定流"""
    items = [b for b in broadcasts if b["is_live"] and b["full_url"]]
    if index < 1 or index > len(items):
        print(f"❌ 无效序号，有效范围: 1-{len(items)}")
        return

    b = items[index - 1]
    url = b["full_url"]
    print(f"🎬 播放: {b['emoji']} {b['name']} ({b['time']})")

    # 按优先级尝试播放器
    players = [
        ("iina", ["iina", "--no-stdin", url]),
        ("mpv", ["mpv", url]),
        ("vlc", ["vlc", url]),
        ("/Applications/IINA.app/Contents/MacOS/iina-cli", ["/Applications/IINA.app/Contents/MacOS/iina-cli", "--no-stdin", url]),
    ]

    for name, cmd in players:
        if shutil.which(cmd[0]) or (cmd[0].startswith("/") and shutil.which(cmd[0])):
            print(f"  ▸ 使用 {name}")
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return

    # 没找到播放器，尝试 macOS open 命令
    print("  ▸ 使用系统默认播放器")
    subprocess.Popen(["open", url])


# ─── 主入口 ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ioctv24.com 直播流抓取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 ioctv_grabber.py                  # 列出所有直播
  python3 ioctv_grabber.py --filter NBA     # 只看 NBA
  python3 ioctv_grabber.py --filter 다저스  # 搜索道奇队
  python3 ioctv_grabber.py --play 1         # 播放第1个
  python3 ioctv_grabber.py --m3u            # 生成 M3U 文件
  python3 ioctv_grabber.py --save streams.json # 保存流地址 JSON
  python3 ioctv_grabber.py --refresh-emoji-cache # 强制刷新联赛emoji缓存
  python3 ioctv_grabber.py --json           # JSON 输出
        """,
    )
    parser.add_argument("--all", action="store_true", help="显示所有频道（含未开播）")
    parser.add_argument("--filter", "-f", type=str, help="按关键字过滤（支持比赛名/联赛名）")
    parser.add_argument("--play", "-p", type=int, help="直接播放第 N 个直播流")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--m3u", nargs="?", const="ioctv_live.m3u", help="生成 M3U 播放列表文件")
    parser.add_argument("--save", nargs="?", const="ioctv_streams.json", default="ioctv_streams.json",
                        help="保存流地址到 JSON 文件（默认: ioctv_streams.json）")
    parser.add_argument("--refresh-emoji-cache", action="store_true",
                        help="强制刷新联赛 emoji 缓存")
    parser.add_argument("--workers", type=int, default=8, help="并发数（默认 8）")

    args = parser.parse_args()
    live_only = not args.all

    session = requests.Session()

    try:
        # 1. 获取基础 URL
        print("📡 连接视频服务器...", file=sys.stderr)
        base_url = get_base_url(session)

        # 2. 解析直播列表
        print("📋 获取赛事列表...", file=sys.stderr)
        category_emoji = get_category_emoji_map(session, refresh_cache=args.refresh_emoji_cache)
        broadcasts = parse_broadcast_list(session, category_emoji=category_emoji)

        if not broadcasts:
            print("❌ 未能解析到任何比赛信息，页面结构可能已变更")
            sys.exit(1)

        # 3. 关键字过滤
        if args.filter:
            kw = args.filter.lower()
            broadcasts = [
                b for b in broadcasts
                if kw in b["name"].lower()
                or kw in b["league"].lower()
                or kw in b["emoji"]
            ]
            if not broadcasts:
                print(f"🔍 没有匹配 '{args.filter}' 的比赛")
                sys.exit(0)

        # 4. 获取流地址
        broadcasts = enrich_streams(session, broadcasts, base_url,
                                    live_only=live_only, max_workers=args.workers)

        # 4.1 保存流地址（默认保存）
        if args.save:
            save_stream_urls(broadcasts, filepath=args.save, live_only=live_only)

        # 5. 输出
        if args.json:
            output_json(broadcasts, live_only=live_only)
        elif args.m3u:
            output_m3u(broadcasts, filepath=args.m3u)
        elif args.play is not None:
            if not any(b["full_url"] for b in broadcasts):
                print("❌ 没有可播放的直播流")
                sys.exit(1)
            print_table(broadcasts, live_only=live_only)
            play_stream(broadcasts, args.play)
        else:
            print_table(broadcasts, live_only=live_only)

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 已取消")
        sys.exit(0)


if __name__ == "__main__":
    main()
