# tools/premium_name_vibration.py
import re
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

# Pythagorean mapping
PYTHAG_MAP = {
    **{c: n for c, n in zip("AJS", [1,1,1])},
    **{c: n for c, n in zip("BKT", [2,2,2])},
    **{c: n for c, n in zip("CLU", [3,3,3])},
    **{c: n for c, n in zip("DMV", [4,4,4])},
    **{c: n for c, n in zip("ENW", [5,5,5])},
    **{c: n for c, n in zip("FOX", [6,6,6])},
    **{c: n for c, n in zip("GPY", [7,7,7])},
    **{c: n for c, n in zip("HQZ", [8,8,8])},
    **{c: n for c, n in zip("IR",  [9,9])},
}

# RU→LAT transliteration (same as other tools)
RU_TO_LAT = {
    "А":"A","Б":"B","В":"V","Г":"G","Д":"D","Е":"E","Ё":"E","Ж":"ZH","З":"Z","И":"I","Й":"I",
    "К":"K","Л":"L","М":"M","Н":"N","О":"O","П":"P","Р":"R","С":"S","Т":"T","У":"U","Ф":"F",
    "Х":"H","Ц":"C","Ч":"CH","Ш":"SH","Щ":"SCH","Ъ":"","Ы":"Y","Ь":"","Э":"E","Ю":"YU","Я":"YA",
}

def _normalize_name(name: str) -> str:
    name = re.sub(r"[^A-Za-zА-Яа-яЁё]", "", name or "")
    if not name:
        raise ValueError("Invalid name")
    return name.upper()

def _to_latin(name: str, locale: str) -> str:
    return "".join(RU_TO_LAT.get(ch, ch) for ch in name) if (locale or "en").lower() == "ru" else name

def _reduce_keep_masters(n: int) -> int:
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
        if n in {11, 22, 33}:
            return n
    return n

def calculate_name_vibration(full_name: str, locale: str = "en") -> int:
    """
    Name Vibration = Expression Number of full name (Pythagorean),
    reduced with master-number awareness (11/22/33 kept).
    """
    loc = (locale or "en").lower()
    clean = _normalize_name(full_name)
    lat = _to_latin(clean, loc)
    total = sum(PYTHAG_MAP.get(ch, 0) for ch in lat if ch.isalpha())
    if total == 0:
        raise ValueError("Invalid name")
    return _reduce_keep_masters(total)

def get_name_vibration_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    """
    Fetch deep/emotional localized text from locales:
      TRANSLATIONS[loc]["result_name_vibration"][str(number)]
    Then append premium-aware CTA. No headers or icons injected here.
    """
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_name_vibration") or {}

    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_name_vibration") or {}
        text = en_block.get(str(number), "🔮 Your Name Vibration reading will appear here soon.")

    # Premium-aware CTA (exactly like Passion/Love/Karmic)
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
