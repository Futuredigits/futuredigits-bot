from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, TypedDict

from db import redis


class UserProfile(TypedDict, total=False):
    birthdate: str          # "YYYY-MM-DD" (or your chosen format)
    full_name: str
    updated_at: int


def _key(user_id: int) -> str:
    return f"profile:{user_id}"


async def set_birthdate(user_id: int, birthdate: str) -> None:
    await redis.hset(_key(user_id), mapping={
        "birthdate": birthdate,
        "updated_at": int(datetime.now(timezone.utc).timestamp()),
    })


async def set_full_name(user_id: int, full_name: str) -> None:
    await redis.hset(_key(user_id), mapping={
        "full_name": full_name,
        "updated_at": int(datetime.now(timezone.utc).timestamp()),
    })


async def get_profile(user_id: int) -> UserProfile:
    data = await redis.hgetall(_key(user_id)) or {}
    # redis is decode_responses=True, so values are strings
    prof: UserProfile = {}
    if data.get("birthdate"):
        prof["birthdate"] = data["birthdate"]
    if data.get("full_name"):
        prof["full_name"] = data["full_name"]
    if data.get("updated_at") and str(data["updated_at"]).isdigit():
        prof["updated_at"] = int(data["updated_at"])
    return prof
