import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram import Bot
from notifications import broadcast

admin_router = Router(name="admin")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

@admin_router.message(F.text.regexp(r"^/testnotif(?:\s+(\w+))?$"))
async def test_notifications(message: Message, bot: Bot, regexp: dict):
    if message.from_user.id != OWNER_ID:
        return
    kind = (regexp.group(1) if regexp and regexp.group(1) else "daily").lower()
    await message.answer(f"Sending test broadcast: {kind}")
    await broadcast(bot, kind)
