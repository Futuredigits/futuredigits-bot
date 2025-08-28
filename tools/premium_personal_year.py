from datetime import datetime
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

def _reduce(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _validate(date_str: str) -> tuple[int, int, int]:
    try:
        d, m, y = date_str.strip().split(".")
        day, month, year = int(d), int(m), int(y)
        datetime(year, month, day)  # sanity check
        return day, month, year
    except Exception:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

def calculate_personal_year(date_str: str, for_year: int | None = None) -> int:
    """
    Personal Year = reduce( reduce(day) + reduce(month) + reduce(target_year) ), 1..9
    By default, target year = current calendar year (server time).
    """
    day, month, _ = _validate(date_str)
    ty = for_year or datetime.now().year
    val = _reduce(day) + _reduce(month) + _reduce(ty)
    return _reduce(val)

def get_personal_year_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_personal_year") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_personal_year") or {}
        text = en_block.get(str(number), "🌌 Your Personal Year insight will appear here soon.")

    # Premium tool CTA behavior: Premium → engagement; trial → upsell
    if user_id is not None:
        if is_premium_user(user_id):
            engagement = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
            if engagement:
                text += "\n\n" + engagement
        else:
            cta = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
            if cta:
                text += "\n\n" + cta
    return text
