import os
from aiogram import Router, F
from aiogram.types import Message
from notifications import broadcast

admin_router = Router(name="admin")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

@admin_router.message(F.text.startswith("/testnotif"))
async def test_notifications(message: Message):
    # Only the owner can trigger broadcasts
    if message.from_user.id != OWNER_ID:
        return

    # Usage: /testnotif [daily|moon|love|weekly|winback]
    parts = message.text.split(maxsplit=1)
    kind = parts[1].strip().lower() if len(parts) > 1 else "daily"

    await message.answer(f"Sending test broadcast: {kind}")
    # Use message.bot to avoid needing Bot injection
    await broadcast(message.bot, kind)
