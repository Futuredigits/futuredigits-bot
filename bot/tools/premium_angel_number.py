import re
from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

# Known repeating and mirror patterns we’ll try to match exactly
KNOWN_PATTERNS = {
    # triplets
    "000","111","222","333","444","555","666","777","888","999",
    # quadruples
    "1111","2222","3333","4444","5555",
    # mirrors
    "1010","1212","1221"
}

def _clean_digits(s: str) -> str:
    if not s:
        raise ValueError("Invalid number")
    digits = re.sub(r"[^0-9]", "", s)
    if not digits:
        raise ValueError("Invalid number")
    # trim overly long inputs to a reasonable window (first 6 digits)
    return digits[:6]

def _reduce_keep_masters(n: int) -> int:
    if n in {11, 22, 33}:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
        if n in {11, 22, 33}:
            return n
    return n

def calculate_angel_key(user_input: str) -> str:
    """
    Returns a translation key under result_angel_number:
      - If the cleaned input matches a KNOWN_PATTERN, returns that exact key (e.g., '1111', '1212').
      - Else returns 'core_X' where X is 1..9 based on digit reduction (masters collapse to their single digit here,
        because locales include core_1..core_9 blocks).
    """
    digits = _clean_digits(user_input)

    # Direct pattern hits (we check the *entire* cleaned string)
    if digits in KNOWN_PATTERNS:
        return digits

    # Otherwise map to a core
    total = sum(int(d) for d in digits)
    reduced = _reduce_keep_masters(total)

    # We only have core_1..core_9 in locales; map masters to their single-digit essence
    if reduced in {11, 22, 33}:
        reduced = sum(int(d) for d in str(reduced))
        while reduced > 9:
            reduced = sum(int(d) for d in str(reduced))

    return f"core_{reduced}"

def get_angel_number_result(key: str, user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_angel_number") or {}

    text = block.get(key)
    if not text:
        # graceful fallback: try EN
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_angel_number") or {}
        text = en_block.get(key) or en_block.get("111", "✨ Your angel message will appear here soon.")

    # Premium-aware CTA logic (same pattern as other premium tools)
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
