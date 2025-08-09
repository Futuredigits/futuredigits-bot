from typing import Dict, Any
import os, json

DEFAULT_LOCALE = "en"

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {},
    "ru": {},
}

_user_locale: Dict[int, str] = {}

def load_locales() -> None:
    """Load locales/en.json and locales/ru.json into TRANSLATIONS."""
    base = os.path.join(os.path.dirname(__file__), "locales")
    for code in ("en", "ru"):
        path = os.path.join(base, f"{code}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    TRANSLATIONS[code] = json.load(f)
                except Exception:
                    
                    TRANSLATIONS[code] = TRANSLATIONS.get(code, {}) or {}

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


__all__ = ["_", "get_text", "get_locale", "set_locale", "TRANSLATIONS", "DEFAULT_LOCALE", "load_locales"]


load_locales()
