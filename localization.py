from typing import Dict, Any

DEFAULT_LOCALE = "en"

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {},
    "ru": {},
}

_user_locale: Dict[int, str] = {}

def set_locale(user_id: int, locale: str) -> None:
    _user_locale[user_id] = locale

def get_locale(user_id: int) -> str:
    return _user_locale.get(user_id, DEFAULT_LOCALE)

def get_text(key: str, locale: str = None, **kwargs: Any) -> str:
    loc = locale or DEFAULT_LOCALE
    text = TRANSLATIONS.get(loc, {}).get(key) \
        or TRANSLATIONS.get(DEFAULT_LOCALE, {}).get(key) \
        or key
    return text.format(**kwargs) if kwargs else text

_ = get_text
