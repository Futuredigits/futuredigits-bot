import re
from localization import get_locale, TRANSLATIONS

# Pythagorean mapping for A–Z
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

# Vowels in EN and RU (for Soul Urge)
VOWELS_EN = set("AEIOUY")
VOWELS_RU = set("АЕЁИОУЫЭЮЯ")

# Minimal transliteration RU->EN for numerology mapping
RU_TO_LAT = {
    "А":"A","Б":"B","В":"V","Г":"G","Д":"D","Е":"E","Ё":"E","Ж":"ZH","З":"Z","И":"I","Й":"I",
    "К":"K","Л":"L","М":"M","Н":"N","О":"O","П":"P","Р":"R","С":"S","Т":"T","У":"U","Ф":"F",
    "Х":"H","Ц":"C","Ч":"CH","Ш":"SH","Щ":"SCH","Ъ":"","Ы":"Y","Ь":"","Э":"E","Ю":"YU","Я":"YA",
}

def _normalize_name(name: str) -> str:
    # Keep letters + spaces/hyphens for validation; remove digits/symbols
    name = re.sub(r"[^A-Za-zА-Яа-яЁё \-]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def _to_latin_for_mapping(name: str, locale: str) -> str:
    if locale == "ru":
        out = []
        for ch in name.upper():
            if ch == " " or ch == "-":
                out.append(ch)
            else:
                out.append(RU_TO_LAT.get(ch, ch))
        return "".join(out)
    return name.upper()

def _sum_vowel_values(name_lat_upper: str, locale: str) -> int:
    if locale == "ru":
        # For vowel detection we need to check original RU characters
        # So we’ll separately build a RU-uppercase version
        pass
    return sum(PYTHAG_MAP.get(ch, 0) for ch in name_lat_upper if ch in VOWELS_EN)

def calculate_soul_urge_number(full_name: str, locale: str = "en") -> int:
    """
    Soul Urge (Heart's Desire): sum values of VOWELS only.
    Supports EN directly and RU via transliteration for values,
    while checking vowels by locale.
    """
    if not full_name or len(full_name) < 2:
        raise ValueError("Invalid name")

    locale = (locale or "en").lower()
    clean = _normalize_name(full_name)
    if not clean or re.fullmatch(r"[ \-]+", clean):
        raise ValueError("Invalid name")

    # Prepare two parallel forms:
    ru_upper = clean.upper()
    lat_upper = _to_latin_for_mapping(clean, locale)

    total = 0
    for i, ch in enumerate(ru_upper):
        # pick matching latin chunk length 1 (simple mapping already expanded in RU_TO_LAT)
        lat_ch = lat_upper[i] if i < len(lat_upper) else ""
        if locale == "ru":
            if ch in VOWELS_RU:
                # map value via Latin char (use first char of translit chunk)
                # If translit produced multiple chars (e.g., "YA"), take first letter’s value
                letter_for_value = lat_upper[i]
                total += PYTHAG_MAP.get(letter_for_value, 0)
        else:
            if ch in VOWELS_EN:
                total += PYTHAG_MAP.get(ch, 0)

    # master numbers 11, 22 are allowed; otherwise reduce to a single digit
    def reduce_num(n: int) -> int:
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    value = reduce_num(total)
    if value == 0:
        # If no vowels were found (rare edge case), fall back to reducing full name vowels as Y-only rule:
        raise ValueError("Invalid name")
    return value

def get_soul_urge_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = locale or (get_locale(user_id) if user_id is not None else "en")
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_soul_urge") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_soul_urge") or {}
        text = en_block.get(str(number), "✨ Your Soul Urge insight will appear here soon.")
    cta = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
    if cta:
        text += "\n\n" + cta
    return text
