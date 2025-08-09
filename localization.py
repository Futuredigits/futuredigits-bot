# localization.py
import json, os
from typing import Dict, Any

DEFAULT_LOCALE = "en"

TRANSLATIONS: Dict[str, Dict[str, Any]] = {"en": {}, "ru": {}}
_user_locale: Dict[int, str] = {}

def load_locales():
    base = os.path.join(os.path.dirname(__file__), "locales")
    for loc in ("en", "ru"):
        path = os.path.join(base, f"{loc}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                TRANSLATIONS[loc] = json.load(f)

def set_locale(user_id: int, locale: str) -> None:
    if locale not in TRANSLATIONS:
        locale = DEFAULT_LOCALE
    _user_locale[user_id] = locale

def get_locale(user_id: int) -> str:
    return _user_locale.get(user_id, DEFAULT_LOCALE)

def get_text(key: str, locale: str = None, **kwargs: Any) -> str:
    loc = locale or DEFAULT_LOCALE
    value = TRANSLATIONS.get(loc, {}).get(key)
    if value is None:
        value = TRANSLATIONS.get(DEFAULT_LOCALE, {}).get(key, key)
    if isinstance(value, str):
        return value.format(**kwargs) if kwargs else value
    return value  # may be dict (for payloads)

# nested payload helper (e.g., result maps)
def get_payload(locale: str, *keys: str):
    d = TRANSLATIONS.get(locale) or TRANSLATIONS[DEFAULT_LOCALE]
    for k in keys:
        d = d.get(k, {})
    return d or {}

_ = get_text
