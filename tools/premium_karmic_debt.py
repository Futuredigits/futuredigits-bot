from localization import get_locale, TRANSLATIONS
from handlers.common import is_premium_user

KD_SET = {13, 14, 16, 19}
KD_TO_REDUCED = {13: 4, 14: 5, 16: 7, 19: 1}

def _reduce_stack(n: int) -> list[int]:
    """Return the chain of reductions (excluding master numbers 11/22/33 for KD detection)."""
    seq = []
    while n > 9 and n not in {11, 22, 33}:
        seq.append(n)
        n = sum(int(d) for d in str(n))
    seq.append(n)
    return seq

def calculate_karmic_debts(date_str: str) -> list[int]:
    """
    Detect KD 13/14/16/19 from:
    - Day of birth (DD),
    - Any intermediate sum in the full date (DD+MM+YYYY digits) reduction chain.
    Returns a sorted unique list.
    """
    try:
        day_s, month_s, year_s = date_str.strip().split(".")
        day, month, year = int(day_s), int(month_s), int(year_s)
    except Exception:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

    debts = set()

    # Rule 1: birthday itself
    if day in KD_SET:
        debts.add(day)

    # Rule 2: intermediate sums in Life Path reduction chain
    digits = [int(d) for d in f"{day:02d}{month:02d}{year}"]
    total = sum(digits)
    chain = _reduce_stack(total)  # includes initial total and successive reductions
    for val in chain:
        if val in KD_SET:
            debts.add(val)

    return sorted(debts)

def get_karmic_debt_result(debts: list[int], user_id: int | None = None, locale: str | None = None) -> str:
    loc = (locale or (get_locale(user_id) if user_id is not None else "en")).lower()
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_karmic_debt") or {}

    # NEW: localized intros
    intro_with = (TRANSLATIONS.get(loc, {}) or {}).get("karmic_debt_intro_with", "")
    intro_none = (TRANSLATIONS.get(loc, {}) or {}).get("karmic_debt_intro_none", "")

    parts = []
    if debts:
        if intro_with:
            parts.append(intro_with)
        for kd in debts:
            text = block.get(str(kd))
            if not text:
                en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_karmic_debt") or {}
                text = en_block.get(str(kd), f"🔹 Karmic Debt {kd}")
            parts.append(text)
    else:
        if intro_none:
            parts.append(intro_none)
        text = block.get("none")
        if not text:
            en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_karmic_debt") or {}
            text = en_block.get("none", "✨ No specific karmic debt numbers detected. You carry lessons of presence, patience, and conscious choice.")
        parts.append(text)

    result = "\n\n".join(parts)

    # CTA logic (same as before)
    if user_id is not None:
        if not is_premium_user(user_id):
            cta = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
            if cta:
                result += "\n\n" + cta
        else:
            engagement = (TRANSLATIONS.get(loc, {}) or {}).get("cta_explore_more", "")
            if engagement:
                result += "\n\n" + engagement

    return result

