from localization import get_locale, TRANSLATIONS

def calculate_life_path_number(date_str: str) -> int:
    try:
        day, month, year = map(int, date_str.strip().split("."))
    except Exception:
        raise ValueError("Invalid date format. Use DD.MM.YYYY.")

    digits = [int(d) for d in f"{day:02d}{month:02d}{year}"]
    total = sum(digits)

    def reduce_to_life_path(n: int) -> int:
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce_to_life_path(total)


def get_life_path_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    # Resolve locale like birthday.py does
    loc = locale or (get_locale(user_id) if user_id is not None else "en")

    # Pull localized block; fallback to EN; fallback to a safe default
    block = (TRANSLATIONS.get(loc, {}) or {}).get("result_life_path") or {}
    text = block.get(str(number))
    if not text:
        en_block = (TRANSLATIONS.get("en", {}) or {}).get("result_life_path") or {}
        text = en_block.get(str(number), "✨ Your Life Path insight will appear here soon.")

    # Append localized CTA if present
    cta_text = (TRANSLATIONS.get(loc, {}) or {}).get("cta_try_more", "")
    if cta_text:
        text += "\n\n" + cta_text

    return text
