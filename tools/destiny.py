# tools/destiny.py
import re
from localization import get_locale, TRANSLATIONS
from tools.expression import calculate_expression_number
from tools.life_path import calculate_life_path_number

DATE_RE = re.compile(r"(.*)\s+(\d{2}\.\d{2}\.\d{4})$")

def parse_name_and_birthdate(text: str) -> tuple[str, str]:
    """
    Expect: 'Full Name DD.MM.YYYY' (name may contain spaces/hyphens).
    """
    m = DATE_RE.match(text.strip())
    if not m:
        raise ValueError("Invalid input")
    full_name = m.group(1).strip()
    date_str = m.group(2)
    if len(full_name) < 2:
        raise ValueError("Invalid input")
    return full_name, date_str

def _reduce(n: int) -> int:
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def calculate_destiny_number(full_name: str, date_str: str, locale: str = "en") -> int:
    """
    Destiny here = reduced(sum(Expression, Life Path)) with master 11/22/33 preserved.
    (Your intro says it combines name and birthdate.)
    """
    expr = calculate_expression_number(full_name, locale=locale)
    life = calculate_life_path_number(date_str)
    total = expr + life
    return _reduce(total)

def get_destiny_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_destiny") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_destiny") or {}
        text = en_block.get(str(number), "🌟 Your Destiny insight will appear here soon.")
    cta = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
    if cta:
        text += "\n\n" + cta
    return text
