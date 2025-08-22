import os
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from notifications import broadcast, send_to_user, _to_int
from db import redis
from notifications import _scheduler as NOTIF_SCHED

admin_router = Router(name="admin")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # set in Render

@admin_router.message(Command("ping"))
async def ping(message: Message):
    await message.answer("pong ✅")

@admin_router.message(Command("whoami"))
async def whoami(message: Message):
    from aiogram.enums import ParseMode
    await message.answer(
        f"<b>Your Telegram user id:</b> {message.from_user.id}<br><b>OWNER_ID env:</b> {OWNER_ID}",
        parse_mode=ParseMode.HTML
    )


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


@admin_router.message(Command("fixsubs"))
async def fixsubs(message: Message):
    if OWNER_ID not in (0, message.from_user.id):
        await message.answer("Not allowed.")
        return
    ids = await redis.smembers("subs:all")
    from notifications import _to_int
    cleaned = {str(_to_int(i)) for i in ids if _to_int(i)}
    # replace the set with normalized entries
    await redis.delete("subs:all")
    for cid in cleaned:
        await redis.sadd("subs:all", cid)
    n = await redis.scard("subs:all")
    await message.answer(f"subs:all normalized. size = {n}")


@admin_router.message(Command("jobs"))
async def jobs(message: Message):
    if OWNER_ID not in (0, message.from_user.id):
        return
    if NOTIF_SCHED is None:
        await message.answer("Scheduler not started.")
        return
    lines = []
    for j in NOTIF_SCHED.get_jobs():
        lines.append(f"• {j.id} → next: {j.next_run_time}")
    await message.answer("Scheduled jobs:\n" + "\n".join(lines))

@admin_router.message(Command("run"))
async def run_now(message: Message):
    # Usage: /run daily | love | moon | weekly | winback
    if OWNER_ID not in (0, message.from_user.id):
        return
    args = (message.text or "").split()
    kind = args[1].lower() if len(args) > 1 else "daily"
    if kind not in {"daily","love","moon","weekly","winback"}:
        await message.answer("Usage: /run [daily|love|moon|weekly|winback]")
        return
    sent, total = await broadcast(message.bot, kind)
    await message.answer(f"Ran '{kind}': sent {sent}/{total} ✅")
