#!/usr/bin/env python3
"""
Danmaku API (PostgreSQL)

Run:
  export DATABASE_URL='postgresql://user:password@host:5432/dbname'
  python3 -m uvicorn danmaku_api:app --host 0.0.0.0 --port 8787 --reload
"""

from __future__ import annotations

import os
import re
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional

import psycopg
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
CONFIG_ENV_FILE = BASE_DIR / "danmaku_api.env"


def read_database_url() -> str:
    """
    读取数据库连接串（优先级）:
    1) 当前目录配置文件 danmaku_api.env
    2) 环境变量 DATABASE_URL
    """
    if CONFIG_ENV_FILE.exists():
        try:
            for raw in CONFIG_ENV_FILE.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "DATABASE_URL":
                    value = v.strip().strip('"').strip("'")
                    if value:
                        return value
        except Exception:
            pass
    return os.getenv("DATABASE_URL", "").strip()


DATABASE_URL = read_database_url()
AUTO_INIT_SCHEMA = os.getenv("AUTO_INIT_SCHEMA", "1").strip() == "1"

HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

SCHEMA_SQL = """
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
"""


class DanmakuCreate(BaseModel):
    video_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=200)
    color: str = Field(default="#ffffff", min_length=7, max_length=7)
    user_name: Optional[str] = Field(default=None, max_length=64)


class DanmakuOut(BaseModel):
    id: int
    video_id: str
    message: str
    color: str
    user_name: Optional[str]
    created_at: datetime


app = FastAPI(title="IOCTV Danmaku API", version="1.0.0")

# Allow local static pages to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files from project root.
app.mount("/static", StaticFiles(directory=str(BASE_DIR)), name="static")


def ensure_database_url() -> None:
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Please create ./danmaku_api.env "
            "with DATABASE_URL=postgresql://..."
        )


@contextmanager
def db_conn() -> Generator[psycopg.Connection, None, None]:
    ensure_database_url()
    with psycopg.connect(DATABASE_URL) as conn:
        yield conn


def normalize_color(color: str) -> str:
    c = (color or "").strip()
    if not HEX_COLOR_RE.match(c):
        return "#ffffff"
    return c.lower()


@app.on_event("startup")
def on_startup() -> None:
    if not AUTO_INIT_SCHEMA:
        return
    try:
        with db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_SQL)
            conn.commit()
    except Exception as e:
        # Keep API process alive even if DB is temporarily unavailable.
        # Requests touching DB will return explicit errors until DB recovers.
        print(f"[startup] warning: schema init skipped: {e}")


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html")


@app.post("/api/danmaku", response_model=DanmakuOut)
def create_danmaku(payload: DanmakuCreate) -> DanmakuOut:
    video_id = payload.video_id.strip()
    message = payload.message.strip()

    if not video_id:
        raise HTTPException(status_code=400, detail="video_id is required")
    if not message:
        raise HTTPException(status_code=400, detail="message is required")

    color = normalize_color(payload.color)
    user_name = payload.user_name.strip() if payload.user_name else None

    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO danmaku_messages (video_id, message, color, user_name)
                VALUES (%s, %s, %s, %s)
                RETURNING id, video_id, message, color, user_name, created_at
                """,
                (video_id, message, color, user_name),
            )
            row = cur.fetchone()
        conn.commit()

    if not row:
        raise HTTPException(status_code=500, detail="insert failed")
    return DanmakuOut(
        id=row[0],
        video_id=row[1],
        message=row[2],
        color=row[3],
        user_name=row[4],
        created_at=row[5],
    )


@app.get("/api/danmaku")
def list_danmaku(
    video_id: str = Query(min_length=1, max_length=128),
    limit: int = Query(default=50, ge=1, le=200),
    after_id: int = Query(default=0, ge=0),
) -> dict:
    vid = video_id.strip()
    if not vid:
        raise HTTPException(status_code=400, detail="video_id is required")

    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, video_id, message, color, user_name, created_at
                FROM danmaku_messages
                WHERE video_id = %s
                  AND id > %s
                ORDER BY id ASC
                LIMIT %s
                """,
                (vid, after_id, limit),
            )
            rows = cur.fetchall()

    items = [
        {
            "id": r[0],
            "video_id": r[1],
            "message": r[2],
            "color": r[3],
            "user_name": r[4],
            "created_at": r[5].isoformat() if r[5] else None,
        }
        for r in rows
    ]
    return {"items": items}
