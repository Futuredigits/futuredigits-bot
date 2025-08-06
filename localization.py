import json

with open("locales/en.json", "r", encoding="utf-8") as f:
    EN = json.load(f)
with open("locales/ru.json", "r", encoding="utf-8") as f:
    RU = json.load(f)

# Temp in-memory dict (replace with DB later)
user_languages = {}

def get_user_lang(user_id: int) -> str:
    return user_languages.get(user_id, "en")

def set_user_lang(user_id: int, lang: str):
    user_languages[user_id] = lang

def get_text(key: str, user_id: int) -> str:
    lang = get_user_lang(user_id)
    return RU.get(key) if lang == "ru" else EN.get(key)
