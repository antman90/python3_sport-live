#!/bin/zsh
set -uo pipefail

WORKDIR="/Users/kingkim/my_data/my_skill"
LOGDIR="$WORKDIR/logs"
LOGFILE="$LOGDIR/uvicorn_supervisor.log"

mkdir -p "$LOGDIR"
cd "$WORKDIR"

while true; do
  echo "[$(date '+%F %T')] starting uvicorn" >> "$LOGFILE"
  python3 -m uvicorn danmaku_api:app --host 0.0.0.0 --port 8787 >> "$LOGFILE" 2>&1
  code=$?
  echo "[$(date '+%F %T')] uvicorn exited code=$code, restart in 3s" >> "$LOGFILE"
  sleep 3
done
