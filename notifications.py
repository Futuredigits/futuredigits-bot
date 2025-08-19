from typing import Iterable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from db import redis
from localization import get_locale, _  # your i18n
from handlers.common import is_premium_user, build_premium_menu  # existing
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timezone, timedelta


from tools.premium_daily_vibe import get_daily_universal_vibe_forecast
from tools.premium_moon_energy import get_moon_energy_result


SUBS_KEY = "subs:all"  # set of chat_ids
LAST_ACTIVE_HASH = "subs:last_active"  # hash: { user_id: last_active_iso }


async def add_subscriber(user_id: int):
    await redis.sadd(SUBS_KEY, user_id)
    await redis.hset(LAST_ACTIVE_HASH, user_id, datetime.now(timezone.utc).isoformat())

async def iter_subscribers() -> Iterable[int]:
    ids = await redis.smembers(SUBS_KEY)
    for uid in ids or []:
        try:
            yield int(uid)
        except:
            continue

# --- CTA button builder (inline)
def build_notif_cta_btn(premium: bool, loc: str) -> InlineKeyboardMarkup:
    text = _("cta_button_explore", locale=loc) if premium else _("cta_button_unlock", locale=loc)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data="open_premium")]
    ])

# --- Message composers
def teaser_text(kind: str, loc: str) -> str:
    if kind == "daily":
        return _("notif_free_teaser_daily", locale=loc)
    if kind == "moon":
        return _("notif_free_teaser_moon", locale=loc)
    if kind == "love":
        return _("notif_free_teaser_love", locale=loc)
    if kind == "weekly":
        return _("notif_free_teaser_weekly", locale=loc)
    if kind == "winback":
        return _("notif_free_winback", locale=loc)
    return "✨"


async def compose_message(user_id: int, kind: str, loc: str) -> tuple[str, InlineKeyboardMarkup]:
    premium = is_premium_user(user_id)
    kb = build_notif_cta_btn(premium, loc)

    if premium:
        if kind == "daily":
            return get_daily_universal_vibe_forecast(user_id=user_id, locale=loc), kb
        if kind == "moon":
            return get_moon_energy_result(user_id=user_id, locale=loc), kb
        if kind == "love":
            # Love Vibes needs a name; use a soft prompt (content lives in locales)
            return _("notif_premium_love_prompt", locale=loc), kb
        if kind == "weekly":
            return _("notif_premium_weekly_ready", locale=loc), kb
        if kind == "winback":
            return _("notif_premium_winback", locale=loc), kb
    else:
        return teaser_text(kind, loc), kb


async def find_inactive(days: int) -> list[int]:
    now = datetime.now(timezone.utc)
    raw = await redis.hgetall(LAST_ACTIVE_HASH) or {}
    out = []
    for uid, iso in raw.items():
        try:
            ts = datetime.fromisoformat(iso)
            if now - ts >= timedelta(days=days):
                out.append(int(uid))
        except Exception:
            continue
    return out


# --- Broadcasters
async def broadcast(bot: Bot, kind: str):
    async for uid in iter_subscribers():
        loc = get_locale(uid)
        text, kb = await compose_message(uid, kind, loc)
        try:
            await bot.send_message(uid, text, reply_markup=kb)
        except Exception:
            # ignore users who blocked the bot or other send errors
            continue

async def broadcast_segment(bot: Bot, kind: str, user_ids: list[int]):
    for uid in user_ids:
        loc = get_locale(uid)
        text, kb = await compose_message(uid, kind, loc)
        try:
            await bot.send_message(uid, text, reply_markup=kb)
        except Exception:
            continue


# --- Scheduler
_scheduler: AsyncIOScheduler | None = None

def init_notifications(bot: Bot):
    global _scheduler
    if _scheduler:
        return _scheduler

    _scheduler = AsyncIOScheduler(timezone=timezone("Europe/Vilnius"))

    # 08:00 daily vibe (all users)
    _scheduler.add_job(
        lambda: bot.loop.create_task(broadcast(bot, "daily")),
        CronTrigger(hour=8, minute=0),
        id="daily_vibe_0800",
        replace_existing=True,
    )

    # 20:00 moon energy (all users)
    _scheduler.add_job(
        lambda: bot.loop.create_task(broadcast(bot, "moon")),
        CronTrigger(hour=20, minute=0),
        id="moon_2000",
        replace_existing=True,
    )

    # 12:30 Mon/Wed/Fri love-vibes nudge (all users)
    _scheduler.add_job(
        lambda: bot.loop.create_task(broadcast(bot, "love")),
        CronTrigger(day_of_week="mon,wed,fri", hour=12, minute=30),
        id="love_1230_mwf",
        replace_existing=True,
    )

        # Sunday 17:00 — weekly upsell/ready ping (all users)
    _scheduler.add_job(
        lambda: bot.loop.create_task(broadcast(bot, "weekly")),
        CronTrigger(day_of_week="sun", hour=17, minute=0),
        id="weekly_upsell_sun_1700",
        replace_existing=True,
    )

    # Daily 11:00 — win-back (FREE users inactive 3+ days)
    async def run_winback():
        uids = await find_inactive(days=3)
        if not uids:
            return
        await broadcast_segment(bot, "winback", uids)

    _scheduler.add_job(
        lambda: bot.loop.create_task(run_winback()),
        CronTrigger(hour=11, minute=0),
        id="winback_1100",
        replace_existing=True,
    )


    _scheduler.start()
    return _scheduler
