#!/bin/zsh
set -euo pipefail

WORKDIR="/Users/kingkim/my_data/my_skill"
LOCKDIR="$WORKDIR/.ioctv_fetch.lock"
LOGFILE="$WORKDIR/ioctv_fetch.log"
RETENTION_DAYS=2

prune_old_logs() {
  [[ -f "$LOGFILE" ]] || return 0
  python3 - "$LOGFILE" "$RETENTION_DAYS" <<'PY'
import re
import sys
from datetime import datetime, timedelta

logfile = sys.argv[1]
retention_days = int(sys.argv[2])
cutoff = datetime.now() - timedelta(days=retention_days)
ts_re = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]")

with open(logfile, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

keep = []
current_should_keep = False
for line in lines:
    m = ts_re.match(line)
    if m:
        try:
            ts = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
            current_should_keep = ts >= cutoff
        except ValueError:
            current_should_keep = False
    if current_should_keep:
        keep.append(line)

with open(logfile, "w", encoding="utf-8") as f:
    f.writelines(keep)
PY
}

prune_old_logs

if ! mkdir "$LOCKDIR" 2>/dev/null; then
  echo "[$(date '+%F %T')] skip: previous job still running" >> "$LOGFILE"
  exit 0
fi

cleanup() {
  rmdir "$LOCKDIR" 2>/dev/null || true
}
trap cleanup EXIT

cd "$WORKDIR"
echo "[$(date '+%F %T')] start fetch" >> "$LOGFILE"

python3 "ioctv_grabber.py" --save "ioctv_streams.json" --workers 8 >> "$LOGFILE" 2>&1

echo "[$(date '+%F %T')] done fetch" >> "$LOGFILE"
