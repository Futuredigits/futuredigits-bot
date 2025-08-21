import os
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from notifications import broadcast, send_to_user, _to_int
from db import redis

admin_router = Router(name="admin")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # set in Render

@admin_router.message(Command("ping"))
async def ping(message: Message):
    await message.answer("pong ✅")

@admin_router.message(Command("whoami"))
async def whoami(message: Message):
    await message.answer(f"Your Telegram user id: {message.from_user.id}\nOWNER_ID env: {OWNER_ID}")

@admin_router.message(Command("subscribe_me"))
async def subscribe_me(message: Message):
    # subscribe the caller so broadcasts can reach them
    from notifications import add_subscriber
    await add_subscriber(message.from_user.id)
    await message.answer("Subscribed to notifications ✅")

@admin_router.message(Command("subcount"))
async def subcount(message: Message):
    n = await redis.scard("subs:all")
    await message.answer(f"subs:all size = {n}")

@admin_router.message(Command("testme"))
async def testme(message: Message, command: CommandObject):
    # send a single notification to yourself (no Redis needed)
    kind = (command.args or "daily").strip().lower()
    from notifications import send_to_user
    await send_to_user(message.bot, message.from_user.id, kind)
    await message.answer(f"Sent to you: {kind} ✅")

@admin_router.message(Command("testnotif"))
async def test_notifications(message: Message, command: CommandObject):
    if OWNER_ID not in (0, message.from_user.id):
        await message.answer("Not allowed.")
        return

    kind = (command.args or "daily").strip().lower()
    if kind not in {"daily", "moon", "love", "weekly", "winback"}:
        await message.answer("Usage: /testnotif [daily|moon|love|weekly|winback]")
        return

    sent, total = await broadcast(message.bot, kind)
    await message.answer(f"Broadcast '{kind}': sent {sent}/{total} ✅")

@admin_router.message(Command("listsubs"))
async def list_subs(message: Message):
    ids = await redis.smembers("subs:all")
    cleaned = sorted(_to_int(i) for i in ids if _to_int(i))
    await message.answer(f"Raw: {list(ids)}\nCleaned: {cleaned}")



