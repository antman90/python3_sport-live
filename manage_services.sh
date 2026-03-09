#!/bin/zsh
set -euo pipefail

WORKDIR="/Users/kingkim/my_data/my_skill"
RUNDIR="$WORKDIR/.run"
LOGDIR="$WORKDIR/logs"
UV_PID_FILE="$RUNDIR/uvicorn_supervisor.pid"
HTTP_PID_FILE="$RUNDIR/http_supervisor.pid"

mkdir -p "$RUNDIR" "$LOGDIR"
cd "$WORKDIR"

is_pid_alive() {
  local pid="$1"
  [[ -n "$pid" ]] || return 1
  kill -0 "$pid" 2>/dev/null
}

start_one() {
  local name="$1"
  local cmd="$2"
  local pid_file="$3"

  if [[ -f "$pid_file" ]]; then
    local old_pid
    old_pid="$(<"$pid_file")"
    if is_pid_alive "$old_pid"; then
      echo "$name already running (pid=$old_pid)"
      return 0
    fi
  fi

  nohup $cmd >/dev/null 2>&1 &
  local new_pid=$!
  echo "$new_pid" > "$pid_file"
  echo "started $name (pid=$new_pid)"
}

stop_one() {
  local name="$1"
  local pid_file="$2"
  if [[ ! -f "$pid_file" ]]; then
    echo "$name not running"
    return 0
  fi
  local pid
  pid="$(<"$pid_file")"
  if is_pid_alive "$pid"; then
    kill "$pid" || true
    sleep 1
    if is_pid_alive "$pid"; then
      kill -9 "$pid" || true
    fi
    echo "stopped $name (pid=$pid)"
  else
    echo "$name stale pid removed"
  fi
  rm -f "$pid_file"
}

status_one() {
  local name="$1"
  local pid_file="$2"
  if [[ -f "$pid_file" ]]; then
    local pid
    pid="$(<"$pid_file")"
    if is_pid_alive "$pid"; then
      echo "$name: running (pid=$pid)"
      return
    fi
  fi
  echo "$name: stopped"
}

case "${1:-}" in
  start)
    start_one "uvicorn-supervisor" "./daemon_uvicorn.sh" "$UV_PID_FILE"
    start_one "http-supervisor" "./daemon_http.sh" "$HTTP_PID_FILE"
    ;;
  stop)
    stop_one "uvicorn-supervisor" "$UV_PID_FILE"
    stop_one "http-supervisor" "$HTTP_PID_FILE"
    ;;
  restart)
    "$0" stop
    "$0" start
    ;;
  status)
    status_one "uvicorn-supervisor" "$UV_PID_FILE"
    status_one "http-supervisor" "$HTTP_PID_FILE"
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac
