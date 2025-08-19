import os
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from notifications import broadcast

admin_router = Router(name="admin")

# Read from the ENV VAR named OWNER_ID (set this in Render)
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

@admin_router.message(Command("ping"))
async def ping(message: Message):
    await message.answer("pong ✅")

@admin_router.message(Command("whoami"))
async def whoami(message: Message):
    await message.answer(f"Your Telegram user id: {message.from_user.id}\nOWNER_ID env: {OWNER_ID}")

@admin_router.message(Command("testnotif"))
async def test_notifications(message: Message, command: CommandObject):
    # Allow only the owner (or allow if OWNER_ID not set yet == 0)
    if OWNER_ID not in (0, message.from_user.id):
        await message.answer("Not allowed.")
        return

    # /testnotif [daily|moon|love|weekly|winback]
    kind = (command.args or "daily").strip().lower()
    if kind not in {"daily", "moon", "love", "weekly", "winback"}:
        await message.answer("Usage: /testnotif [daily|moon|love|weekly|winback]")
        return

    await message.answer(f"Sending test broadcast: {kind}")
    await broadcast(message.bot, kind)
