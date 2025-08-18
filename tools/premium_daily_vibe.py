from datetime import datetime, timezone
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

def _reduce_single(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _universal_day(today: datetime | None = None) -> int:
    d = (today or datetime.now(timezone.utc)).date()
    total = sum(int(x) for x in f"{d.year:04d}{d.month:02d}{d.day:02d}")
    return _reduce_single(total)

# cache: (date, locale, ud) -> core text WITHOUT CTA
_CORE_CACHE: dict[tuple[str, str, int], str] = {}

def _today_iso() -> str:
    return datetime.now(timezone.utc).date().isoformat()

def get_daily_universal_vibe_result(ud: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    today = _today_iso()
    ck = (today, loc, ud)

    core = _CORE_CACHE.get(ck)
    if core is None:
        # 1) Get body text
        block = (TRANSLATIONS.get(loc, {}) or {}).get("result_daily_vibe") or {}
        body = block.get(str(ud))
        if not body:
            en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_daily_vibe") or {}
            body = en_block.get(str(ud), "✨ Your Daily Vibe reading will appear here soon.")

        # 2) Build header (label + emoji) — no intro injection here
        prefix = (TRANSLATIONS.get(loc, {}) or {}).get("daily_vibe_prefix", "")
        emojis = (TRANSLATIONS.get(loc, {}) or {}).get("daily_vibe_emojis") or {}
        icon = emojis.get(str(ud), "")

        header = f"{icon} {prefix} {ud}".strip()

        # 3) If body ends with the same icon, strip it to avoid duplicate emoji
        if icon and body.rstrip().endswith(icon):
            body = body.rstrip()[:-len(icon)].rstrip()

        core = f"{header}\n\n{body}"
        _CORE_CACHE[ck] = core

    # CTA (not cached)
    result = core
    if user_id is not None:
        if is_premium_user(user_id):
            tail = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
        else:
            tail = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
        if tail:
            result += "\n\n" + tail

    return result

def get_daily_universal_vibe_forecast(user_id: int | None = None, locale: str | None = None) -> str:
    ud = _universal_day()
    return get_daily_universal_vibe_result(ud, user_id=user_id, locale=locale)
