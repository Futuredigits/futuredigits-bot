from datetime import datetime, timezone
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

# --- Core: Universal Day (reduced to 1..9) ---
def _reduce_single(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _universal_day(today: datetime | None = None) -> int:
    d = (today or datetime.now(timezone.utc)).date()
    total = sum(int(x) for x in f"{d.year:04d}{d.month:02d}{d.day:02d}")
    return _reduce_single(total)  # 1..9

# --- Per-day cache for core text (intro + label + result), no CTA ---
# key: (date_iso, locale, ud) -> str
_CORE_CACHE: dict[tuple[str, str, int], str] = {}

def _today_iso() -> str:
    return datetime.now(timezone.utc).date().isoformat()

def get_daily_universal_vibe_result(ud: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    today = _today_iso()
    ck = (today, loc, ud)

    core = _CORE_CACHE.get(ck)
    if core is None:
        block = (TRANSLATIONS.get(loc, {}) or {}).get("result_daily_vibe") or {}
        text = block.get(str(ud))
        if not text:
            en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_daily_vibe") or {}
            text = en_block.get(str(ud), "✨ Your Daily Vibe reading will appear here soon.")

        # Intro
        intro = (TRANSLATIONS.get(loc, {}) or {}).get("intro_daily_vibe", "")
        if intro:
            text = intro + "\n\n" + text

        # Label + emoji (optional)
        prefix = (TRANSLATIONS.get(loc, {}) or {}).get("daily_vibe_prefix", "")
        emojis = (TRANSLATIONS.get(loc, {}) or {}).get("daily_vibe_emojis") or {}
        if prefix:
            icon = emojis.get(str(ud), "")
            lead = f"{icon} " if icon else ""
            text = f"{lead}{prefix} {ud}\n\n{text}"

        core = text
        _CORE_CACHE[ck] = core

    # Append CTA per-user (not cached)
    result = core
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

# Back-compat shim expected by common.py
def get_daily_universal_vibe_forecast(user_id: int | None = None, locale: str | None = None) -> str:
    ud = _universal_day()
    return get_daily_universal_vibe_result(ud, user_id=user_id, locale=locale)
