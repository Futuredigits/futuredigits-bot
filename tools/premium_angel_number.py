from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user
import re

def _digits_only(s: str) -> str:
    if s is None:
        raise ValueError("Empty input")
    seq = re.sub(r"[^0-9]", "", str(s))
    if not seq:
        raise ValueError("No digits in input")
    return seq

def _reduce(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _classify(seq: str) -> str:
    """
    Canonical translation key:
    - exact repeats: 111, 222, ..., 999 (any len >=2)
    - portals: 1111, 2222, 3333, 4444, 5555
    - mirrors/patterns: 000, 1010, 1212, 1221, 1313..1919
    - fallback: core_<1..9> (digital root)
    """
    if set(seq) == {"0"} and len(seq) >= 2:
        return "000"

    # exact repeats (non-zero)
    if len(set(seq)) == 1 and seq[0] != "0":
        if seq in {
            "11","111","1111","22","222","2222","33","333","3333",
            "44","444","4444","55","555","5555","66","666","6666",
            "77","777","7777","88","888","8888","99","999","9999"
        }:
            return seq
        return seq[0] * 3

    if seq in {"1010","1212","1221","1313","1414","1515","1616","1717","1818","1919"}:
        return seq

    if seq in {"1111","2222","3333","4444","5555"}:
        return seq

    root = _reduce(int(seq))
    return f"core_{root}"

def decode_angel_number(raw: str) -> str:
    seq = _digits_only(raw)
    return _classify(seq)

def get_angel_number_result(raw: str, user_id: int | None = None, locale: str | None = None) -> str:
    key = decode_angel_number(raw)
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()

    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_angel_number") or {}
    text = block.get(key)
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_angel_number") or {}
        text = en_block.get(key)

    if not text:
        # final fallback (still premium‑tone)
        if key.startswith("core_"):
            num = key.split("_", 1)[1]
            text = {
                "1": "✨ Lead bravely. Make the first move; the path appears under your feet.",
                "2": "🤝 Choose harmony. Ask for help, offer help, trust the weave.",
                "3": "🎨 Create freely. Humor and art heal faster than perfection.",
                "4": "🏗️ Build it. Consistency over intensity; structure sets you free.",
                "5": "🌬️ Embrace change. Innovate, travel, or learn—fresh air for the soul.",
                "6": "💞 Tend your people. Love plus responsibility equals peace.",
                "7": "🌌 Go inward. Study, pray, journal—clarity blooms in quiet.",
                "8": "💎 Own your impact. Negotiate fairly; respect your time and energy.",
                "9": "🌙 Let go. Forgive, finish, and make room for the new.",
            }.get(num, "✨ You’re guided. Breathe, listen, and follow the small yes in your chest.")
        else:
            text = "✨ You’re guided. Breathe, listen, and follow the small yes in your chest."

    # Premium-aware CTA (same behavior as Personal Year). :contentReference[oaicite:1]{index=1}
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
