from __future__ import annotations

from datetime import datetime, timedelta
from localization import TRANSLATIONS

def _reduce(n: int) -> int:
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _universal_day_number(dt: datetime) -> int:
    digits = f"{dt.day:02d}{dt.month:02d}{dt.year}"
    return _reduce(sum(int(x) for x in digits))

def get_week_map(*, user_id: int, locale: str = "en") -> str:
    """MVP 7-day map. Personalization comes in Step 2."""
    loc = (locale or "en").lower()
    t = TRANSLATIONS.get(loc, {}) or TRANSLATIONS.get("en", {})

    title = t.get("week_title", "🗓 Your 7‑Day Map")
    subtitle = t.get("week_subtitle", "Use this to plan: best days to push, and days to keep it quiet.")

    start = datetime.now()
    rows = []
    for i in range(7):
        d = start + timedelta(days=i)
        n = _universal_day_number(d)
        label = d.strftime("%a %d.%m")
        rows.append((label, n))

    lines = "\n".join([f"• *{label}*: {n}" for label, n in rows])
    note = t.get("week_note", "Premium adds: the best/worst day for money, love, and hard conversations.")
    return f"{title}\n{subtitle}\n\n{lines}\n\n{note}"
