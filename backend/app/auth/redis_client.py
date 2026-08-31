# app/auth/redis_client.py
from datetime import datetime, timezone

import redis

from app.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)


def _key(user_id: int, jti: str) -> str:
    return f"refresh_token:{user_id}:{jti}"


def store_refresh_token(user_id: int, jti: str, expires_at: datetime) -> None:
    ttl_seconds = int((expires_at - datetime.now(timezone.utc)).total_seconds())
    redis_client.set(_key(user_id, jti), "1", ex=max(ttl_seconds, 1))


def is_refresh_token_valid(user_id: int, jti: str) -> bool:
    return redis_client.exists(_key(user_id, jti)) == 1


def revoke_refresh_token(user_id: int, jti: str) -> None:
    redis_client.delete(_key(user_id, jti))
