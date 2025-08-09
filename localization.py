import os
import json
from typing import Dict, Any

DEFAULT_LOCALE = "en"

TRANSLATIONS: Dict[str, Dict[str, Any]] = {"en": {}, "ru": {}}
_user_locale: Dict[int, str] = {}

def _load_translations() -> None:
    base_dir = os.path.dirname(__file__)
    locales_dir = os.path.join(base_dir, "locales")
    for loc in ("en", "ru"):
        path = os.path.join(locales_dir, f"{loc}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                TRANSLATIONS[loc] = json.load(f)
        except Exception:
            
            TRANSLATIONS[loc] = TRANSLATIONS.get(loc, {})


_load_translations()

def set_locale(user_id: int, locale: str) -> None:
    if locale not in TRANSLATIONS:
        locale = DEFAULT_LOCALE
    _user_locale[user_id] = locale

def get_locale(user_id: int) -> str:
    return _user_locale.get(user_id, DEFAULT_LOCALE)

def get_text(key: str, locale: str | None = None, **kwargs: Any) -> Any:
    """Return localized value (string or complex type) with EN fallback."""
    loc = locale or DEFAULT_LOCALE
    raw = (
        TRANSLATIONS.get(loc, {}).get(key)
        or TRANSLATIONS.get(DEFAULT_LOCALE, {}).get(key)
        or key
    )
    if isinstance(raw, str):
        return raw.format(**kwargs) if kwargs else raw
    # For dicts/lists/etc — return as-is
    return raw
