#!/bin/bash
set -u

# =============================
# 配置区
# =============================
# 本地 JSON 文件路径（只同步这个文件）
LOCAL_FILE="/Users/kingkim/my_data/my_skill/ioctv_streams.json"

# Ubuntu 服务器 SSH 用户名和 IP
REMOTE_USER="root"
REMOTE_HOST="146.88.131.114"
REMOTE_PORT="10370"

# 服务器目标目录
REMOTE_DIR="/var/www/www_python/livetv01"

# 日志文件路径
LOG_FILE="/Users/kingkim/my_data/my_skill/json_sync.log"

# 日志保留天数
MAX_LOG_DAYS=7

# rsync 超时时间（秒）
RSYNC_TIMEOUT=30

# 是否只使用 scp（1=是，0=否）
FORCE_SCP_ONLY=1

# 远程完整文件路径
REMOTE_FILE="${REMOTE_DIR}/$(basename "$LOCAL_FILE")"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" >> "${LOG_FILE}"
}

# =============================
# 日志轮转：删除超过 MAX_LOG_DAYS 的旧日志
# =============================
find "$(dirname "$LOG_FILE")" -name "$(basename "$LOG_FILE")*" -mtime +$MAX_LOG_DAYS -delete

if [[ ! -f "${LOCAL_FILE}" ]]; then
  log "ERROR: 本地文件不存在: ${LOCAL_FILE}"
  exit 1
fi

# =============================
# 确保远程目录存在
# =============================
if ! ssh -p "${REMOTE_PORT}" "${REMOTE_USER}@${REMOTE_HOST}" "mkdir -p '${REMOTE_DIR}'"; then
  log "ERROR: 远程目录创建失败: ${REMOTE_DIR}"
  exit 1
fi

# =============================
# 同步 JSON 文件
# =============================

RSYNC_BIN="$(command -v rsync || true)"
if [[ -z "${RSYNC_BIN}" && -x "/opt/homebrew/bin/rsync" ]]; then
  RSYNC_BIN="/opt/homebrew/bin/rsync"
fi

SYNC_OK=0

if [[ "${FORCE_SCP_ONLY}" -eq 1 ]]; then
  log "INFO: FORCE_SCP_ONLY=1，跳过 rsync，直接使用 scp"
elif [[ -n "${RSYNC_BIN}" ]]; then
  echo "rsync: ${RSYNC_BIN}" >> "${LOG_FILE}"
  if "${RSYNC_BIN}" -avz --update --progress --timeout="${RSYNC_TIMEOUT}" \
      -e "ssh -p ${REMOTE_PORT}" \
      "${LOCAL_FILE}" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILE}" \
      >> "${LOG_FILE}" 2>&1; then
    SYNC_OK=1
    log "JSON 文件已通过 rsync 同步到 ${REMOTE_HOST}:${REMOTE_FILE}"
  else
    log "WARN: rsync 同步失败，尝试回退到 scp"
  fi
else
  log "WARN: 本地未找到 rsync，尝试使用 scp"
fi

if [[ "${SYNC_OK}" -ne 1 ]]; then
  if scp -P "${REMOTE_PORT}" -o ConnectTimeout="${RSYNC_TIMEOUT}" \
      "${LOCAL_FILE}" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILE}" \
      >> "${LOG_FILE}" 2>&1; then
    SYNC_OK=1
    log "JSON 文件已通过 scp 同步到 ${REMOTE_HOST}:${REMOTE_FILE}"
  else
    log "ERROR: scp 同步失败"
    exit 1
  fi
fi

# =============================
# 同步完成时间记录
# =============================
log "同步任务结束"
