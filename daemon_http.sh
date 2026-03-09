#!/bin/zsh
set -uo pipefail

WORKDIR="/Users/kingkim/my_data/my_skill"
LOGDIR="$WORKDIR/logs"
LOGFILE="$LOGDIR/http_supervisor.log"

mkdir -p "$LOGDIR"
cd "$WORKDIR"

while true; do
  echo "[$(date '+%F %T')] starting http.server" >> "$LOGFILE"
  python3 -m http.server 8000 >> "$LOGFILE" 2>&1
  code=$?
  echo "[$(date '+%F %T')] http.server exited code=$code, restart in 3s" >> "$LOGFILE"
  sleep 3
done
