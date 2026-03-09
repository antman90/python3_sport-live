CREATE TABLE IF NOT EXISTS danmaku_messages (
    id BIGSERIAL PRIMARY KEY,
    video_id TEXT NOT NULL,
    message TEXT NOT NULL,
    color VARCHAR(7) NOT NULL DEFAULT '#ffffff',
    user_name VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_danmaku_video_created
ON danmaku_messages (video_id, created_at DESC);
