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

# handlers/admin.py (only the lines with message.answer changed)

@admin_router.message(Command("whoami"))
async def whoami(message: Message):
    await message.answer(
        f"Your Telegram user id: <code>{message.from_user.id}</code>\n"
        f"OWNER_ID env: <code>{OWNER_ID}</code>",
        parse_mode="HTML",
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
    lines = [f"• <code>{j.id}</code> → next: <code>{j.next_run_time}</code>" for j in sched.get_jobs()]
    await message.answer("Scheduled jobs:\n" + "\n".join(lines), parse_mode="HTML")

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
    # No risky markdown in this string, but we can be consistent:
    await message.answer(f"Ran '{kind}': sent {sent}/{total} ✅")

@admin_router.message(Command("subcount"))
async def subcount(message: Message):
    n = await redis.scard("subs:all")
    await message.answer(f"subs:all size = <code>{n}</code>", parse_mode="HTML")

@admin_router.message(Command("listsubs"))
async def list_subs(message: Message):
    ids = await redis.smembers("subs:all")
    # format IDs safely
    cleaned: list[str] = []
    for x in ids:
        s = x.decode() if isinstance(x, bytes) else str(x)
        digits = "".join(ch for ch in s if ch.isdigit())
        if digits:
            cleaned.append(digits)
    cleaned_sorted = ", ".join(sorted(cleaned))
    await message.answer(f"Subscribers: <code>{cleaned_sorted}</code>", parse_mode="HTML")

