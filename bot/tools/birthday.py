from localization import _, get_locale, TRANSLATIONS

def calculate_birthday_number(date_str: str) -> int:
    try:
        day = int(date_str.strip().split('.')[0])
    except:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

    return day if day in {11, 22} else sum(int(d) for d in str(day)) if day > 9 else day


def get_birthday_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = locale or (get_locale(user_id) if user_id is not None else "en")

    block = TRANSLATIONS.get(loc, {}).get("result_birthday") or {}
    text = block.get(str(number))
    if not text:
        en_block = TRANSLATIONS.get("en", {}).get("result_birthday") or {}
        text = en_block.get(str(number), "✨ Your birthday insight will appear here soon.")

    
    cta_text = TRANSLATIONS.get(loc, {}).get("cta_try_more", "")
    if cta_text:
        text += "\n\n" + cta_text

    return text
