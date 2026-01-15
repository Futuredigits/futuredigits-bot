from __future__ import annotations

from datetime import datetime
from localization import TRANSLATIONS

def _reduce(n: int) -> int:
    # simple 1-9 reduction; keep 11/22/33 if ever needed later
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _universal_day_number(dt: datetime) -> int:
    digits = f"{dt.day:02d}{dt.month:02d}{dt.year}"
    return _reduce(sum(int(x) for x in digits))

def get_today_guidance(*, user_id: int, locale: str = "en", premium: bool = False) -> str:
    """MVP 'Today Guidance'. Personalization comes in Step 2 (profile storage)."""
    loc = (locale or "en").lower()
    dt = datetime.now()
    day_num = _universal_day_number(dt)

    # Minimal behavior-first content. We'll move most of this into JSON in Step 2.
    t = TRANSLATIONS.get(loc, {}) or TRANSLATIONS.get("en", {})
    title = t.get("today_title", "🗓 Today’s Guidance")
    teaser = t.get("today_teaser", "You don’t need more motivation today — you need clean focus.")
    key_line = t.get("today_key_line", "🔢 Today’s key number: *{n}*").format(n=day_num)

    if not premium:
        upsell = t.get("today_upsell", "🔒 Premium unlocks: best time window + what to do / avoid for *your* profile.")
        return f"{title}\n\n{teaser}\n\n{key_line}\n\n{upsell}"

    do_line   = t.get("today_do",   "✅ Do: finish one thing that’s been dragging on.")
    dont_line = t.get("today_dont", "⛔ Don’t: start fights, overpromise, or multitask.")
    window    = t.get("today_window", "⏱ Best window: 10:00–13:00 (local time).")
    step      = t.get("today_step", "🎯 Micro-step: pick ONE task and set a 25‑minute timer.")
    return f"{title}\n\n{key_line}\n\n{do_line}\n{dont_line}\n{window}\n\n{step}"
