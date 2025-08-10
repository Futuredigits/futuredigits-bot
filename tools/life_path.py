from localization import TRANSLATIONS, get_locale, _

def get_life_path_result(num: int, user_id: int) -> str:
    loc = get_locale(user_id) or "en"

    # Pull localized result map (fallback to EN only if RU missing the map)
    result_map = TRANSLATIONS.get(loc, {}).get("result_life_path") \
                 or TRANSLATIONS["en"]["result_life_path"]

    # Keys in JSON are strings
    key = str(num)
    text = result_map.get(key)
    if not text:
        # last‑ditch fallback to EN for this specific number
        text = TRANSLATIONS["en"]["result_life_path"].get(key, "…")

    # Single, localized CTA (keep CTA OUT of the JSON result body)
    cta = _("cta_try_more", locale=loc)

    return f"{text}\n\n{cta}"

