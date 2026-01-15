# tools/guidance_today.py
from datetime import datetime
from localization import TRANSLATIONS
from tools.day_type_engine import get_day_type

DAY_TYPE_KEYS = {
    "pressure": "day_pressure",
    "opportunity": "day_opportunity",
    "risk": "day_risk",
    "conflict": "day_conflict",
    "preparation": "day_preparation",
    "transition": "day_transition",
    "quiet_power": "day_quiet_power",
}

def _t(loc: str, key: str, fallback: str = "") -> str:
    return (TRANSLATIONS.get(loc, {}) or {}).get(key) or (TRANSLATIONS.get("en", {}) or {}).get(key) or fallback

def get_today_guidance(*, user_id: int, locale: str, premium: bool = False) -> str:
    loc = (locale or "en").lower()
    now = datetime.now()

    day_type = get_day_type(now)
    block_key = DAY_TYPE_KEYS[day_type]

    # Title shared
    title = _t(loc, "today_title", "🗓 Today’s Guidance")

    # Fetch localized day-type blocks (free + premium)
    free_text = _t(loc, f"{block_key}_free", "")
    premium_text = _t(loc, f"{block_key}_premium", "")

    if premium:
        body = premium_text or free_text
        # Premium ending hook (optional)
        end = _t(loc, "today_premium_end", "")
        if end:
            body = f"{body}\n\n{end}"
    else:
        body = free_text or premium_text
        hook = _t(loc, "today_free_hook", "🔒 Premium reveals why this day hits *you* and what shifts tomorrow.")
        body = f"{body}\n\n{hook}"

    return f"{title}\n\n{body}"
