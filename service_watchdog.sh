#!/bin/zsh
set -euo pipefail

WORKDIR="/Users/kingkim/my_data/my_skill"
LOGFILE="$WORKDIR/logs/watchdog.log"

mkdir -p "$WORKDIR/logs"
cd "$WORKDIR"

timestamp() {
  date '+%F %T'
}

ensure_supervisors_running() {
  ./manage_services.sh start >> "$LOGFILE" 2>&1
}

check_http() {
  curl -fsS --max-time 4 "http://127.0.0.1:8000/ioctv_streams_viewer.html" >/dev/null
}

check_api() {
  curl -fsS --max-time 4 "http://127.0.0.1:8787/api/health" >/dev/null
}

echo "[$(timestamp)] watchdog tick" >> "$LOGFILE"
ensure_supervisors_running

if ! check_http; then
  echo "[$(timestamp)] http check failed, restarting supervisors" >> "$LOGFILE"
  ./manage_services.sh restart >> "$LOGFILE" 2>&1
fi

if ! check_api; then
  echo "[$(timestamp)] api check failed, restarting supervisors" >> "$LOGFILE"
  ./manage_services.sh restart >> "$LOGFILE" 2>&1
fi
