from localization import _, get_locale, TRANSLATIONS

def calculate_birthday_number(date_str: str) -> int:
    try:
        day = int(date_str.strip().split('.')[0])
    except:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

    return day if day in {11, 22} else sum(int(d) for d in str(day)) if day > 9 else day


def get_birthday_result(number: int, user_id: int | None = None, locale: str | None = None) -> str:
    loc = locale or (get_locale(user_id) if user_id else "en")

    # Prefer localized JSON payload if present
    try:
        results = TRANSLATIONS.get(loc, {}).get("result_birthday") or TRANSLATIONS["en"]["result_birthday"]
        text = results.get(str(number))
        if text:
            return text
    except Exception:
        pass


    text = results.get(number, "⚠️ An error occurred while calculating your Birthday Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"
