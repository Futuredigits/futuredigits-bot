import os
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

import notifications as notif
from notifications import init_notifications, broadcast
from db import redis

admin_router = Router(name="admin")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

def is_owner(msg: Message) -> bool:
    return OWNER_ID == 0 or (msg.from_user and msg.from_user.id == OWNER_ID)

@admin_router.message(Command("whoami"))
async def whoami(message: Message):
    await message.answer(
        f"Your Telegram user id: {message.from_user.id}\nOWNER_ID env: {OWNER_ID}"
    )

@admin_router.message(Command("jobs"))
async def jobs(message: Message):
    if not is_owner(message):
        await message.answer("Not allowed.")
        return
    sched = notif._scheduler
    if sched is None:
        await message.answer("Scheduler not started. Use /startjobs to boot it.")
        return
    lines = [f"• {j.id} → next: {j.next_run_time}" for j in sched.get_jobs()]
    await message.answer("Scheduled jobs:\n" + "\n".join(lines))

@admin_router.message(Command("startjobs"))
async def startjobs(message: Message):
    if not is_owner(message):
        await message.answer("Not allowed.")
        return
    sched = init_notifications(message.bot)
    await message.answer("Scheduler started ✅" if sched else "Failed to start scheduler")

@admin_router.message(Command("run"))
async def run_now(message: Message, command: CommandObject):
    if not is_owner(message):
        await message.answer("Not allowed.")
        return
    kind = (command.args or "daily").strip().lower()
    if kind not in {"daily", "love", "moon", "weekly", "winback"}:
        await message.answer("Usage: /run [daily|love|moon|weekly|winback]")
        return
    sent, total = await broadcast(message.bot, kind)
    await message.answer(f"Ran '{kind}': sent {sent}/{total} ✅")

@admin_router.message(Command("subscribe_me"))
async def subscribe_me(message: Message):
    # Quick helper to add yourself to the broadcast set
    from notifications import add_subscriber
    await add_subscriber(message.from_user.id)
    await message.answer("Subscribed to notifications ✅")

@admin_router.message(Command("subcount"))
async def subcount(message: Message):
    n = await redis.scard("subs:all")
    await message.answer(f"subs:all size = {n}")

@admin_router.message(Command("listsubs"))
async def list_subs(message: Message):
    ids = await redis.smembers("subs:all")
    cleaned = sorted(int(x) for x in ids if str(x).isdigit() or str(x).strip().isdigit())
    await message.answer(f"Subscribers: {cleaned}")
