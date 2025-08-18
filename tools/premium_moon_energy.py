from datetime import datetime, timezone
from math import floor
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

# --- Moon phase calculation (8 phases) ---
# 0 New, 1 Waxing Crescent, 2 First Quarter, 3 Waxing Gibbous,
# 4 Full, 5 Waning Gibbous, 6 Last Quarter, 7 Waning Crescent
_EPOCH = datetime(2001, 1, 1, 0, 0, 0, tzinfo=timezone.utc)  # near a known new moon
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
    cycle = (days % _SYNODIC_DAYS) / _SYNODIC_DAYS  # 0..1
    idx = floor(cycle * 8 + 0.5) % 8
    return idx

def get_today_moon_phase_key() -> str:
    return PHASE_KEYS[_moon_phase_index()]

# --- Lightweight daily cache for core text (without CTA) ---
# key = (date_iso, locale, phase_key) -> str
_CORE_CACHE: dict[tuple[str, str, str], str] = {}

def _today_iso_for_cache() -> str:
    # If you later add per-user timezones, compute date in that TZ here
    return datetime.now(timezone.utc).date().isoformat()

def get_moon_energy_result(
    phase_key: str | None = None,
    user_id: int | None = None,
    locale: str | None = None
) -> str:
    """
    Build today's Moon Energy reading:
      - Intro (intro_moon_energy)
      - 'Moon phase: <Name>' with emoji
      - Deep phase text (result_moon_energy[phase])
      - Premium-aware CTA appended per user
    Core text is cached per day/locale/phase; CTA is not cached.
    """
    key = phase_key or get_today_moon_phase_key()
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()

    today_iso = _today_iso_for_cache()
    cache_key = (today_iso, loc, key)

    core_text = _CORE_CACHE.get(cache_key)
    if core_text is None:
        # Phase result
        block = (TRANSLATIONS.get(loc, {}) or {}).get("result_moon_energy") or {}
        text = block.get(key)
        if not text:
            en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_moon_energy") or {}
            text = en_block.get(key, "🌙 Your Moon Energy reading will appear here soon.")

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

        core_text = text
        _CORE_CACHE[cache_key] = core_text

    # Append CTA per-user (not cached)
    result = core_text
    if user_id is not None:
        if is_premium_user(user_id):
            engagement = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
            if engagement:
                result += "\n\n" + engagement
        else:
            upsell = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
            if upsell:
                result += "\n\n" + upsell

    return result

# Back-compat shim expected by handlers/common.py
def get_moon_energy_forecast(
    user_id: int | None = None,
    locale: str | None = None,
    phase_key: str | None = None
) -> str:
    return get_moon_energy_result(phase_key=phase_key, user_id=user_id, locale=locale)
