# 反分析绕过、协议与加密还原、CTF 自动解题、Web 逆向与接口追踪
调用skill reverse-multi-track，处理https://ioctv24.com, 爬取网站到当前文件夹

# 基本用法 - 列出所有正在直播的频道和 m3u8 地址
python3 ioctv_grabber.py

# 按关键字过滤
python3 ioctv_grabber.py --filter NBA
python3 ioctv_grabber.py --filter WBC

# 直接播放第 N 个（自动找 IINA/mpv/VLC）
python3 ioctv_grabber.py --play 9

# 生成 M3U 播放列表文件（VLC/IINA 直接打开）
python3 ioctv_grabber.py --m3u

# JSON 输出（方便其他程序调用）
python3 ioctv_grabber.py --json

# 显示所有频道（含未开播的）
python3 ioctv_grabber.py --all

## 定时抓取（每分钟）

已提供脚本：
`fetch_live_streams.sh`

功能：
- 每次抓取直播频道和 m3u8 地址
- 输出到 `ioctv_streams.json`
- 防重入锁（上一次未完成时跳过）
- 日志写入 `ioctv_fetch.log`

已安装 cron：
`* * * * * /Users/kingkim/my_data/my_skill/fetch_live_streams.sh # ioctv-live-fetch`

## Danmaku PostgreSQL API

Install:
```bash
pip3 install -r requirements.txt
```

<!-- DB_HOST_pgFulive=192.168.3.36
DB_PORT_pgFulive=5432
DB_DATABASE_pgFulive=db_fulive
DB_USERNAME_pgFulive=role_fulive
DB_PASSWORD_pgFulive=kingsai003 -->
Run API:
```bash
# 1) 在当前目录创建配置文件 danmaku_api.env
# DATABASE_URL=postgresql://user:password@host:5432/dbname
#
# 2) 前台运行（调试，页面+接口同端口）
python3 -m uvicorn danmaku_api:app --host 0.0.0.0 --port 8000 --reload
```

Schema file:
`db/danmaku_schema.sql`

Endpoints:
- `POST /api/danmaku`
  - body: `{"video_id":"74","message":"hello","color":"#ffffff","user_name":"guest"}`
- `GET /api/danmaku?video_id=74&after_id=0&limit=50`

Frontend:
- main page file: `index.html` (same-origin API)
- You can override by setting: `window.IOCTV_API_BASE`

#### 页面
```
http://127.0.0.1:8000
```

#### 接口
```
http://127.0.0.1:8000/api/health
```

#### 定时任务(一分钟执行一次)
```
* * * * * /Users/kingkim/my_data/my_skill/fetch_live_streams.sh # ioctv-live-fetch
```

#### 后台守护（异常自动重启）
```
# 启动守护进程（uvicorn 单进程提供页面+接口）
./manage_services.sh start

# 查看状态
./manage_services.sh status

# 停止
./manage_services.sh stop

# 每分钟健康检查（异常自动拉起/重启）
# 已安装:
# * * * * * /Users/kingkim/my_data/my_skill/service_watchdog.sh # ioctv-service-watchdog
```

#### 本地电脑抓取数据，同步到114服务器
```
* * * * * /Users/kingkim/my_data/my_skill/sync_json.sh # ioctv-json-sync
```

#### 更新rsync
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew --version # Homebrew 5.0.16

brew upgrade rsync

# 安装完成后，Homebrew 的 rsync 路径通常是：
# Apple Silicon（M1/M2）：/opt/homebrew/bin/rsync
# Intel Mac：/usr/local/bin/rsync

# 你可以把这一行加到 ~/.zshrc 或 ~/.bash_profile，保证每次终端启动都使用新版 rsync。
# Apple Silicon
export PATH="/opt/homebrew/bin:$PATH"

# Intel Mac
# export PATH="/usr/local/bin:$PATH"
```

#### 页面访问地址
##### 页面：http://127.0.0.1:8000/static/index.html
##### 接口健康检查：http://127.0.0.1:8000/api/health

```
server {
    listen 443 ssl http2;
    server_name live.example.com;

    ssl_certificate     /etc/letsencrypt/live/live.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/live.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name live.example.com;
    return 301 https://$host$request_uri;
}
```