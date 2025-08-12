from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

def _reduce(n: int) -> int:
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _life_path(date_str: str) -> int:
    day, month, year = [int(x) for x in date_str.split(".")]
    total = sum(int(d) for d in f"{day:02d}{month:02d}{year}")
    return _reduce(total)

def calculate_compatibility(date1: str, date2: str) -> int:
    """
    Compatibility = reduced sum of both Life Path Numbers (keeping master numbers).
    """
    lp1 = _life_path(date1)
    lp2 = _life_path(date2)
    total = lp1 + lp2
    return _reduce(total)

def get_compatibility_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_compatibility") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_compatibility") or {}
        text = en_block.get(str(number), "❤️ Your compatibility reading will appear here soon.")

    # CTA logic — upsell for non-premium, engagement for premium
    if user_id is not None:
        if not is_premium_user(user_id):
            cta = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
            if cta:
                text += "\n\n" + cta
        else:
            engagement = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
            if engagement:
                text += "\n\n" + engagement

    return text
