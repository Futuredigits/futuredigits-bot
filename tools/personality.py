import re
from localization import get_locale, TRANSLATIONS

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

VOWELS_EN = set("AEIOUY")
VOWELS_RU = set("АЕЁИОУЫЭЮЯ")

RU_TO_LAT = {
    "А":"A","Б":"B","В":"V","Г":"G","Д":"D","Е":"E","Ё":"E","Ж":"ZH","З":"Z","И":"I","Й":"I",
    "К":"K","Л":"L","М":"M","Н":"N","О":"O","П":"P","Р":"R","С":"S","Т":"T","У":"U","Ф":"F",
    "Х":"H","Ц":"C","Ч":"CH","Ш":"SH","Щ":"SCH","Ъ":"","Ы":"Y","Ь":"","Э":"E","Ю":"YU","Я":"YA",
}

def _normalize_name(name: str) -> str:
    name = re.sub(r"[^A-Za-zА-Яа-яЁё \-]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    if not name or re.fullmatch(r"[ \-]+", name):
        raise ValueError("Invalid name")
    return name

def _to_latin(name: str, locale: str) -> str:
    if locale == "ru":
        out = []
        for ch in name.upper():
            if ch in (" ", "-"):
                out.append(ch)
            else:
                out.append(RU_TO_LAT.get(ch, ch))
        return "".join(out)
    return name.upper()

def _is_vowel(ch_ru_upper: str, locale: str) -> bool:
    return (ch_ru_upper in VOWELS_RU) if locale == "ru" else (ch_ru_upper in VOWELS_EN)

def calculate_personality_number(full_name: str, locale: str = "en") -> int:
    """
    Personality number = sum of CONSONANTS' values (Pythagorean).
    RU supported by vowel detection in RU and value mapping via transliteration.
    """
    locale = (locale or "en").lower()
    clean = _normalize_name(full_name)
    ru_upper = clean.upper()
    lat_upper = _to_latin(clean, locale)

    total = 0
    # Walk through characters in parallel; for RU multi-letter translits, take the FIRST letter’s value
    li = 0
    for ch in ru_upper:
        if ch in (" ", "-"):
            li += 1
            continue
        # detect vowel in the RU/EN domain
        if not _is_vowel(ch, locale):  # consonants only
            # pick first Latin letter for value
            lat_ch = lat_upper[li] if li < len(lat_upper) else ""
            total += PYTHAG_MAP.get(lat_ch, 0)
        # advance latin index at least by 1
        li += 1

    if total == 0:
        raise ValueError("Invalid name")

    def reduce_num(n: int) -> int:
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce_num(total)

def get_personality_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_personality") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_personality") or {}
        text = en_block.get(str(number), "🎭 Your Personality insight will appear here soon.")
    cta = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
    if cta:
        text += "\n\n" + cta
    return text
