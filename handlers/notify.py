from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from db import redis

SUBS_KEY = "subs:all"
LAST_ACTIVE_HASH = "subs:last_active"

notify_router = Router(name="notify")

@notify_router.message(Command("stop"))
async def stop_notifs(message: Message):
    uid = str(message.from_user.id)
    await redis.srem(SUBS_KEY, uid)
    await redis.hdel(LAST_ACTIVE_HASH, uid)
    await message.answer("🔕 Notifications turned off.\nSend /start anytime to turn them back on.")
