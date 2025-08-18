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
    Build today's Moon Energy message with a clean layout:
      - Header: "<emoji> <moon_phase_prefix> <Phase Name>"
      - Body:   result_moon_energy[phase] (no intro)
      - CTA:    premium-aware (appended per-user)
    Core text is cached per day/locale/phase; CTA is not cached.
    """
    key = phase_key or get_today_moon_phase_key()
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()

    today_iso = _today_iso_for_cache()
    cache_key = (today_iso, loc, key)

    core_text = _CORE_CACHE.get(cache_key)
    if core_text is None:
        # --- Body (no intro injection) ---
        block = (TRANSLATIONS.get(loc, {}) or {}).get("result_moon_energy") or {}
        body = block.get(key)
        if not body:
            en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_moon_energy") or {}
            body = en_block.get(key, "🌙 Your Moon Energy reading will appear here soon.")

        # --- Header (emoji + label + phase name) ---
        label = (TRANSLATIONS.get(loc, {}) or {}).get("moon_phase_prefix", "")
        names = (TRANSLATIONS.get(loc, {}) or {}).get("moon_phase_names") or {}
        emojis = (TRANSLATIONS.get(loc, {}) or {}).get("moon_phase_emojis") or {}
        phase_name = names.get(key, "")
        phase_emoji = emojis.get(key, "")

        header_parts = []
        if phase_emoji:
            header_parts.append(phase_emoji)
        if label:
            header_parts.append(label)
        if phase_name:
            header_parts.append(phase_name)
        header = " ".join(p for p in header_parts if p).strip()

        # --- Prevent duplicate emoji at the end of the body ---
        if phase_emoji and body.rstrip().endswith(phase_emoji):
            body = body.rstrip()[:-len(phase_emoji)].rstrip()

        core_text = f"{header}\n\n{body}"
        _CORE_CACHE[cache_key] = core_text

    # --- CTA (not cached) ---
    result = core_text
    if user_id is not None:
        if is_premium_user(user_id):
            tail = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
        else:
            tail = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
        if tail:
            result += "\n\n" + tail

    return result

# Back-compat shim expected by handlers/common.py
def get_moon_energy_forecast(
    user_id: int | None = None,
    locale: str | None = None,
    phase_key: str | None = None
) -> str:
    return get_moon_energy_result(phase_key=phase_key, user_id=user_id, locale=locale)
