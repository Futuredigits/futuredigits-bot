# tools/guidance_today.py
from datetime import datetime
from localization import TRANSLATIONS
from tools.day_type_engine import get_day_type
from tools.profile_store import get_profile

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

async def get_today_guidance(*, user_id: int, locale: str, premium: bool = False) -> str:
    loc = (locale or "en").lower()
    now = datetime.now()

    day_type = get_day_type(now)
    block_key = DAY_TYPE_KEYS.get(day_type, "day_pressure")

    title = _t(loc, "today_title", "🗓 Today’s Guidance")

    free_text = _t(loc, f"{block_key}_free", "")
    premium_text = _t(loc, f"{block_key}_premium", "")

    if premium:
        body = premium_text or free_text
        end = _t(loc, "today_premium_end", "")
        if end:
            body = f"{body}\n\n{end}"
    else:
        body = free_text or premium_text
        hook = _t(loc, "today_free_hook", "🔒 Premium reveals why this day hits *you* and what shifts tomorrow.")
        body = f"{body}\n\n{hook}"

        tomorrow = _t(loc, "tomorrow_tease", "")
        if tomorrow:
            body = f"{body}\n\n{tomorrow}"
    
    cons_key = f"{block_key}_consequence_{'premium' if premium else 'free'}"
    cons = _t(loc, cons_key, "")
    if cons:
        body = f"{body}\n\n{cons}"

    profile = await get_profile(user_id)
    has_profile = bool(profile.get("birthdate")) and bool(profile.get("full_name"))


    if has_profile:
        bias_key = "today_bias_premium" if premium else "today_bias_free"
        bias = _t(loc, bias_key, "")
        if bias:
            body = f"{body}\n\n{bias}"


    if has_profile:
        body = f"{body}\n\n{_t(loc, 'profile_ready_line', '✅ Personal layer: active.')}"
    else:
        body = f"{body}\n\n{_t(loc, 'profile_missing_hook', '⚠️ Add Personal Data to unlock your personal layer.')}"


