import re
from collections import Counter
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

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

RU_TO_LAT = {
    "А":"A","Б":"B","В":"V","Г":"G","Д":"D","Е":"E","Ё":"E","Ж":"ZH","З":"Z","И":"I","Й":"I",
    "К":"K","Л":"L","М":"M","Н":"N","О":"O","П":"P","Р":"R","С":"S","Т":"T","У":"U","Ф":"F",
    "Х":"H","Ц":"C","Ч":"CH","Ш":"SH","Щ":"SCH","Ъ":"","Ы":"Y","Ь":"","Э":"E","Ю":"YU","Я":"YA",
}

def _normalize_name(name: str) -> str:
    name = re.sub(r"[^A-Za-zА-Яа-яЁё]", "", name)
    if not name:
        raise ValueError("Invalid name")
    return name.upper()

def _to_latin(name: str, locale: str) -> str:
    if locale == "ru":
        return "".join(RU_TO_LAT.get(ch, ch) for ch in name)
    return name

def _reduce(n: int) -> int:
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def calculate_passion_number(full_name: str, locale: str = "en") -> int:
    loc = (locale or "en").lower()
    clean = _normalize_name(full_name)
    latin = _to_latin(clean, loc)

    # Count frequency of each Pythagorean value
    values = [PYTHAG_MAP.get(ch, 0) for ch in latin if ch.isalpha()]
    freq = Counter(values)
    if not freq:
        raise ValueError("Invalid name")

    # Most frequent number(s)
    max_freq = max(freq.values())
    top_numbers = [n for n, count in freq.items() if count == max_freq and n != 0]

    # If multiple, sum & reduce
    if len(top_numbers) > 1:
        return _reduce(sum(top_numbers))
    return top_numbers[0]

from handlers.common import is_premium_user

def get_passion_number_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_passion_number") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_passion_number") or {}
        text = en_block.get(str(number), "🧩 Your Passion Number insight will appear here soon.")

    if user_id is not None:
        if not is_premium_user(user_id):
            # Non-premium → upsell CTA
            cta = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
            if cta:
                text += "\n\n" + cta
        else:
            # Premium → engagement CTA
            engagement = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
            if engagement:
                text += "\n\n" + engagement

    return text

