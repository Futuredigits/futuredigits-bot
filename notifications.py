from typing import Iterable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

import asyncio
import logging
from pytz import timezone as tz


SCHED_TZ = tz("Europe/Vilnius")

from db import redis
from aiogram.enums import ParseMode
from localization import get_locale, _  
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from datetime import datetime, timedelta, timezone as dt_timezone  
from datetime import date


from tools.premium_daily_vibe import get_daily_universal_vibe_forecast
from tools.premium_moon_energy import get_moon_energy_forecast as get_moon_energy_result


SUBS_KEY = "subs:all"  
LAST_ACTIVE_HASH = "subs:last_active"  # hash: { user_id: last_active_iso }



async def add_subscriber(user_id: int):
    try:
        await redis.sadd(SUBS_KEY, str(user_id))
        await redis.hset(LAST_ACTIVE_HASH, str(user_id), datetime.now(dt_timezone.utc).isoformat()

    except Exception as e:        
        logging.warning("[notif] add_subscriber failed for %s: %s", user_id, e)

async def iter_subscribers() -> Iterable[int]:
    ids = await redis.smembers(SUBS_KEY)
    for uid in ids or []:
        val = _to_int(uid)
        if val:
            yield val



# --- CTA button builder (inline)
def build_notif_cta_btn(premium: bool, loc: str, kind: str | None = None) -> InlineKeyboardMarkup:
    """
    First row: topic deep-link (Daily / Love / Moon)
    Second row: Upgrade (free) or Explore (premium)
    Falls back to Premium menu if kind is unknown.
    """
    mapping = {
        "daily": ("btn_daily", "open_daily"),
        "love":  ("btn_love",  "open_love"),
        "moon":  ("btn_moon",  "open_moon"),
        # weekly/winback: still route them somewhere useful
        "weekly": ("btn_daily", "open_daily"),
        "winback": ("btn_daily", "open_daily"),
        "tomorrow": ("btn_daily", "open_daily"),
    }
    key, cb = mapping.get(kind or "", ("btn_daily", "open_daily"))
    topic_btn = InlineKeyboardButton(text=_(key, locale=loc), callback_data=cb)

    bottom_text = _("cta_button_explore", locale=loc) if premium else _("cta_button_unlock", locale=loc)
    bottom_btn = InlineKeyboardButton(text=bottom_text, callback_data="open_premium")

    return InlineKeyboardMarkup(inline_keyboard=[[topic_btn], [bottom_btn]])


# --- Message composers
def teaser_text(kind: str, loc: str) -> str:
    if kind == "daily":
        keys = ["notif_free_teaser_daily_v1","notif_free_teaser_daily_v2","notif_free_teaser_daily_v3"]
        return _(_pick_key(keys), locale=loc)
    if kind == "moon":
        keys = ["notif_free_teaser_moon_v1","notif_free_teaser_moon_v2","notif_free_teaser_moon_v3"]
        return _(_pick_key(keys), locale=loc)
    if kind == "love":
        keys = ["notif_free_teaser_love_v1","notif_free_teaser_love_v2","notif_free_teaser_love_v3"]
        return _(_pick_key(keys), locale=loc)
    if kind == "tomorrow":  
        keys = ["notif_tomorrow_teaser_v1","notif_tomorrow_teaser_v2","notif_tomorrow_teaser_v3"]
        return _(_pick_key(keys), locale=loc)
    if kind == "weekly":
        return _("notif_free_teaser_weekly", locale=loc)
    if kind == "winback":
        return _("notif_free_winback", locale=loc)
    return "✨"



def _is_premium(user_id: int) -> bool:
    try:
        from handlers.common import is_premium_user  # lazy import to avoid circulars
        return is_premium_user(user_id)
    except Exception:
        return False


def _to_int(user_id_raw):
    try:
        if isinstance(user_id_raw, int):
            return user_id_raw
        if isinstance(user_id_raw, bytes):
            s = user_id_raw.decode(errors="ignore")
        else:
            s = str(user_id_raw)
        digits = "".join(ch for ch in s if ch.isdigit())
        return int(digits) if digits else None
    except Exception:
        return None


def _variant_index(n: int) -> int:
    # Same variant for everyone per day (Europe/Vilnius)
    today = datetime.now(tz("Europe/Vilnius")).timetuple().tm_yday
    return today % n if n > 0 else 0

def _pick_key(keys: list[str]) -> str:
    idx = _variant_index(len(keys))
    return keys[idx]


async def send_to_user(bot, user_id: int, kind: str):
    try:
        loc = get_locale(user_id)
        text, kb = await compose_message(user_id, kind, loc)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=kb, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print(f"[send_to_user] failed for {user_id}: {e}")




async def compose_message(user_id: int, kind: str, loc: str) -> tuple[str, InlineKeyboardMarkup]:
    premium = _is_premium(user_id)
    kb = build_notif_cta_btn(premium, loc, kind)  # <— add kind here

    if premium:
        if kind == "daily":
            return get_daily_universal_vibe_forecast(user_id=user_id, locale=loc), kb
        if kind == "moon":
            return get_moon_energy_result(user_id=user_id, locale=loc), kb
        if kind == "love":
            keys = ["notif_premium_love_prompt_v1","notif_premium_love_prompt_v2","notif_premium_love_prompt_v3"]
            return _(_pick_key(keys), locale=loc), kb
        if kind == "weekly":
            keys = ["notif_premium_weekly_ready_v1","notif_premium_weekly_ready_v2","notif_premium_weekly_ready_v3"]
            return _(_pick_key(keys), locale=loc), kb
        if kind == "winback":
            keys = ["notif_premium_winback_v1","notif_premium_winback_v2","notif_premium_winback_v3"]
            return _(_pick_key(keys), locale=loc), kb
        if kind == "tomorrow":  
            keys = ["notif_tomorrow_premium_v1","notif_tomorrow_premium_v2","notif_tomorrow_premium_v3"]
            return _(_pick_key(keys), locale=loc), kb
    else:
        return teaser_text(kind, loc), kb


async def find_inactive(days: int) -> list[int]:
    now = datetime.now(dt_timezone.utc)
    raw = await redis.hgetall(LAST_ACTIVE_HASH) or {}
    out: list[int] = []
    for uid_raw, iso_raw in raw.items():
        try:
            uid = _to_int(uid_raw)
            if not uid:
                continue
            iso_str = iso_raw.decode() if isinstance(iso_raw, bytes) else str(iso_raw)
            ts = datetime.fromisoformat(iso_str)
            if now - ts >= timedelta(days=days):
                out.append(uid)
        except Exception:
            continue
    return out


# --- Broadcasters
async def broadcast(bot, kind: str):
    try:
        ids = await redis.smembers(SUBS_KEY)
        total = len(ids) if ids else 0
        if total == 0:
            print(f"[broadcast] kind={kind} no subscribers")
            return 0, 0

        sent = 0
        for raw in ids:
            uid = _to_int(raw)
            if not uid:
                continue
            try:
                loc = get_locale(uid)
                text, kb = await compose_message(uid, kind, loc)
                await bot.send_message(chat_id=uid, text=text, reply_markup=kb, parse_mode=ParseMode.MARKDOWN)
                sent += 1

            except Exception as e:
                err = str(e)
                print(f"[broadcast] send failed for {uid}: {err}")                
                if ("Forbidden: bot was blocked by the user" in err) or ("chat not found" in err.lower()):
                    await redis.srem(SUBS_KEY, str(uid))
                    await redis.hdel(LAST_ACTIVE_HASH, str(uid))                
                elif "user is deactivated" in err.lower():
                    await redis.srem(SUBS_KEY, str(uid))
                    await redis.hdel(LAST_ACTIVE_HASH, str(uid))

        print(f"[broadcast] kind={kind} sent={sent} total={total}")
        return sent, total
    except Exception as e:
        print(f"[broadcast] fatal error: {e}")
        return 0, 0



async def broadcast_segment(bot: Bot, kind: str, user_ids: list[int]):
    for uid in user_ids:
        loc = get_locale(uid)
        text, kb = await compose_message(uid, kind, loc)
        try:
            await bot.send_message(uid, text, reply_markup=kb, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            err = str(e)
            print(f"[broadcast_segment] send failed for {uid}: {err}")
            if ("Forbidden: bot was blocked by the user" in err) or ("chat not found" in err.lower()) or ("user is deactivated" in err.lower()):
                await redis.srem(SUBS_KEY, str(uid))
                await redis.hdel(LAST_ACTIVE_HASH, str(uid))
            continue


# --- Scheduler
_scheduler: AsyncIOScheduler | None = None

def init_notifications(bot: Bot):
    global _scheduler
    if _scheduler:
        logging.info("[notif] scheduler already started")
        return _scheduler

    logging.info("[notif] starting scheduler…")
    loop = asyncio.get_event_loop()

    _scheduler = AsyncIOScheduler(
        event_loop=loop,
        timezone=SCHED_TZ,
        job_defaults={"misfire_grace_time": 6 * 3600, "coalesce": True},  # 6h grace, safer on restarts
    )

    # --- jobs
    async def job_daily():
        await broadcast(bot, "daily")

    async def job_love():
        await broadcast(bot, "love")

    async def job_moon():
        await broadcast(bot, "moon")

    async def job_weekly():
        await broadcast(bot, "weekly")

    async def job_tomorrow():
        await broadcast(bot, "tomorrow")

    async def job_winback():
        uids = await find_inactive(days=3)
        logging.info(f"[winback] candidates={len(uids)}")
        if uids:
            await broadcast_segment(bot, "winback", uids)
    
    async def _reconcile_stars():
        try:
            offset = None
            seen = 0
            max_pages = 100  # safety net

            def _calc_exp_ts(tx) -> int:
                exp = tx.get("subscription_expiration_date")
                now = int(datetime.now(dt_timezone.utc).timestamp())
                if isinstance(exp, (int, float)):
                    return int(exp)
                if isinstance(exp, str) and exp.isdigit():
                    return int(exp)
                # fallback: tx.date + 30 days
                tx_date = tx.get("date")
                base = int(tx_date) if isinstance(tx_date, (int, float)) else now
                return base + 30 * 24 * 60 * 60

            pages = 0
            while True:
                pages += 1
                if pages > max_pages:
                    logging.warning("[stars] reconcile stopped: hit page cap (%s)", max_pages)
                    break
            
                resp = await bot.get_star_transactions(limit=100, offset=offset)
            
                txs = getattr(resp, "transactions", None)
                if not txs:
                    txs = resp.get("transactions") if isinstance(resp, dict) else []
                    if not txs:
                        break

                for tx in txs:
                    payload_str = (
                        tx.get("invoice_payload")
                        or (tx.get("invoice") or {}).get("payload")
                        or ""
                    )
                    s = str(payload_str)

                    # Support monthly and lifetime; fall back to legacy monthly-only
                    m = re.match(r"premium:(monthly|lifetime):(\d+):", s)
                    if not m:
                        m = re.match(r"premium:monthly:(\d+):", s)
                        if not m:
                            continue

                    try:
                        uid = int(m.group(2))  # new pattern
                    except IndexError:
                        uid = int(m.group(1))  # legacy pattern

                    exp_ts = _calc_exp_ts(tx)

                    await redis.hset("premium:sub_next_renewal", str(uid), exp_ts)

                    if exp_ts > int(datetime.now(dt_timezone.utc).timestamp()):
                        from handlers.common import PAID_USERS
                        PAID_USERS.add(uid)

                    seen += 1

                # pagination
                offset = getattr(resp, "next_offset", None)
                if not offset and isinstance(resp, dict):
                    offset = resp.get("next_offset")
                if not offset:
                    break

            logging.info("[stars] reconcile done: seen=%s", seen)
            return seen

        except Exception as e:
            logging.exception("[stars] reconcile failed: %s", e)
            return 0

    
    _scheduler.add_job(job_daily,  CronTrigger(hour=8,  minute=0,  timezone=SCHED_TZ), id="daily_vibe_0800",       replace_existing=True, misfire_grace_time=23 * 3600)
    _scheduler.add_job(job_love,   CronTrigger(hour=12, minute=30, timezone=SCHED_TZ), id="love_1230_daily",       replace_existing=True)
    _scheduler.add_job(job_moon,   CronTrigger(hour=20, minute=0,  timezone=SCHED_TZ), id="moon_2000",             replace_existing=True)
    _scheduler.add_job(job_weekly, CronTrigger(day_of_week="sun", hour=17, minute=0, timezone=SCHED_TZ), id="weekly_upsell_sun_1700", replace_existing=True)
    _scheduler.add_job(job_winback,CronTrigger(hour=11, minute=0,  timezone=SCHED_TZ), id="winback_1100",          replace_existing=True)    
    _scheduler.add_job(job_tomorrow, CronTrigger(hour=21, minute=0, timezone=SCHED_TZ), id="tomorrow_teaser_2100", replace_existing=True)

    _scheduler.add_job(_reconcile_stars, CronTrigger(minute="*/30", timezone=SCHED_TZ),
                       id="stars_reconcile_30m", replace_existing=True)
            

    _scheduler.start()
    for j in _scheduler.get_jobs():
        logging.info(f"[notif] job={j.id} next={j.next_run_time}")

    logging.info("[notif] scheduler started ✅")
    return _scheduler







