from datetime import datetime, timezone
from math import floor
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

# ---- Moon phase calculation (8-phase index) ----
# 0 New, 1 Waxing Crescent, 2 First Quarter, 3 Waxing Gibbous,
# 4 Full, 5 Waning Gibbous, 6 Last Quarter, 7 Waning Crescent
#
# Simple, reliable approximation adapted for daily use in apps.
# Good enough for coaching/energy guidance (±1 phase around boundaries).

_EPOCH = datetime(2001, 1, 1, 0, 0, 0, tzinfo=timezone.utc)  # near known new moon
_SYNODIC_DAYS = 29.53058867

PHASE_KEYS = [
    "new_moon",
    "waxing_crescent",
    "first_quarter",
    "waxing_gibbous",
    "full_moon",
    "waning_gibbous",
    "last_quarter",
    "waning_crescent",
]

def _moon_phase_index(dt: datetime | None = None) -> int:
    dt = dt.astimezone(timezone.utc) if dt else datetime.now(timezone.utc)
    days = (dt - _EPOCH).total_seconds() / 86400.0
    # Normalize to 0..1 cycle
    cycle = (days % _SYNODIC_DAYS) / _SYNODIC_DAYS
    # Map to 8 bins
    idx = floor(cycle * 8 + 0.5) % 8
    return idx

def get_today_moon_phase_key() -> str:
    return PHASE_KEYS[_moon_phase_index()]

def get_moon_energy_forecast(user_id: int | None = None, locale: str | None = None, phase_key: str | None = None) -> str:
    """
    Back-compat for common.unified_premium_menu_handler
    """
    return get_moon_energy_result(phase_key=phase_key, user_id=user_id, locale=locale)

# tools/premium_moon_energy.py (essential parts)

def get_moon_energy_result(phase_key: str | None = None, user_id: int | None = None, locale: str | None = None) -> str:
    key = phase_key or get_today_moon_phase_key()
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()

    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_moon_energy") or {}
    text = block.get(key) or (TRANSLATIONS.get("en", {}).get("result_moon_energy") or {}).get(key, "🌙 Your Moon Energy reading will appear here soon.")

    # Intro
    intro = (TRANSLATIONS.get(loc, {}) or {}).get("intro_moon_energy", "")
    if intro:
        text = intro + "\n\n" + text

    # Label + emoji
    label = (TRANSLATIONS.get(loc, {}) or {}).get("moon_phase_prefix", "")
    names = (TRANSLATIONS.get(loc, {}) or {}).get("moon_phase_names") or {}
    emojis = (TRANSLATIONS.get(loc, {}) or {}).get("moon_phase_emojis") or {}
    if label and names:
        phase_name = names.get(key, "")
        phase_emoji = emojis.get(key, "")
        if phase_name:
            prefix = f"{phase_emoji} " if phase_emoji else ""
            text = f"{prefix}{label} {phase_name}\n\n{text}"

    # CTA
    if user_id is not None:
        if is_premium_user(user_id):
            engagement = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
            if engagement:
                text += "\n\n" + engagement
        else:
            upsell = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
            if upsell:
                text += "\n\n" + upsell

    return text




