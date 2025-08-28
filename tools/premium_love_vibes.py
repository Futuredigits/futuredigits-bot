from datetime import datetime
import re
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

# Pythagorean numbers for letters
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

# Treat vowels for Soul Urge
VOWELS = set("AEIOUY")

# Basic RU→LAT transliteration (sufficient for numerology mapping)
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
    if (locale or "en").lower() == "ru":
        return "".join(RU_TO_LAT.get(ch, ch) for ch in name)
    return name

def _reduce_keep_masters(n: int) -> int:
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
        if n in {11, 22, 33}:
            return n
    return n

def _reduce_single(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _soul_urge(full_name: str, locale: str) -> int:
    clean = _normalize_name(full_name)
    lat = _to_latin(clean, locale)
    total = sum(PYTHAG_MAP.get(ch, 0) for ch in lat if ch in VOWELS)
    if total == 0:
        raise ValueError("Invalid name")
    return _reduce_keep_masters(total)

def _universal_day(today: datetime | None = None) -> int:
    d = (today or datetime.now()).date()
    total = sum(int(digit) for digit in f"{d.year:04d}{d.month:02d}{d.day:02d}")
    return _reduce_single(total)  # Universal Day is typically reduced to 1..9

def calculate_love_vibe(full_name: str, locale: str = "en") -> int:
    """
    Love Vibe = reduce_keep_masters(SoulUrge + UniversalDay)
    """
    loc = (locale or "en").lower()
    su = _soul_urge(full_name, loc)
    ud = _universal_day()
    return _reduce_keep_masters(su + ud)

def get_love_vibes_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_love_vibes") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_love_vibes") or {}
        text = en_block.get(str(number), "❤️ Your Love Vibes reading will appear here soon.")

    # Premium tool behavior:
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
