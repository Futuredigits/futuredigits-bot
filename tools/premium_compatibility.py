import re
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

def _normalize(s: str) -> str:
    s = re.sub(r"[^A-Za-zА-Яа-яЁё \-]", "", s or "")
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        raise ValueError("Invalid name")
    return s

def _to_latin(name: str, locale: str) -> str:
    if (locale or "en").lower() == "ru":
        return "".join(RU_TO_LAT.get(ch, ch) for ch in name.upper())
    return name.upper()

def _reduce(n: int) -> int:
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _name_number(full_name: str, locale: str) -> int:
    clean = _normalize(full_name)
    lat = _to_latin(clean, locale)
    total = sum(PYTHAG_MAP.get(ch, 0) for ch in lat if ch.isalpha())
    if total == 0:
        raise ValueError("Invalid name")
    return _reduce(total)

def _compatibility_score(n1: int, n2: int, compat: int) -> int:
    BASE = {1:80,2:90,3:84,4:72,5:82,6:88,7:74,8:76,9:86,11:85,22:78,33:87}
    score = BASE.get(compat, 80)

    if n1 == n2:
        score += 3
    diff = abs(n1 - n2)
    if diff == 1:
        score += 2
    elif diff >= 4:
        score -= 3

    if n1 in {11,22,33} and n2 in {11,22,33}:
        score += 2

    if compat in {11,33}:
        score += 1
    elif compat == 22:
        score += 0

    score = max(55, min(97, score))
    return int(round(score))


def calculate_compatibility(name1: str, name2: str, locale: str = "en") -> tuple[int, int, int, int]:
    """
    Returns (compatibility_number, score_percent, n1, n2)
    """
    loc = (locale or "en").lower()
    n1 = _name_number(name1, loc)
    n2 = _name_number(name2, loc)
    compat = _reduce(n1 + n2)
    score = _compatibility_score(n1, n2, compat)
    return compat, score, n1, n2


def get_compatibility_result(number: int, score: int | None, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_compatibility") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_compatibility") or {}
        text = en_block.get(str(number), "❤️ Your compatibility reading will appear here soon.")

    # Always show score (Premium-only tool)
    label = (TRANSLATIONS.get(loc, {}) or {}).get("compat_score_prefix", "")
    if label and score is not None:
        text = f"{label} {score}%\n\n" + text
    elif score is not None:
        text = f"{score}%\n\n" + text

    # CTA: Premium gets engagement, trial gets upsell
    from handlers.common import is_premium_user
    if user_id is not None and is_premium_user(user_id):
        engagement = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
        if engagement:
            text += "\n\n" + engagement
    else:
        cta = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
        if cta:
            text += "\n\n" + cta

    return text

