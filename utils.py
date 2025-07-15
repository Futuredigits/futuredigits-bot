import datetime
from db import get_user_language
from translations import translations

def is_valid_date(text: str) -> bool:
    try:
        day, month, year = map(int, text.split('.'))
        datetime.datetime(year, month, day)
        return True
    except ValueError:
        return False

def reduce_to_core_number(n: int) -> int:
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

def calculate_expression_number(name: str) -> int:
    letter_map = {
        'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9,
        'j':1, 'k':2, 'l':3, 'm':4, 'n':5, 'o':6, 'p':7, 'q':8, 'r':9,
        's':1, 't':2, 'u':3, 'v':4, 'w':5, 'x':6, 'y':7, 'z':8
    }
    total = sum(letter_map.get(c.lower(), 0) for c in name if c.isalpha())
    return reduce_to_core_number(total)

def calculate_soul_urge_number(name: str) -> int:
    vowels = 'aeiou'
    total = sum(ord(c.lower()) - 96 for c in name if c.lower() in vowels and c.isalpha())
    return reduce_to_core_number(total)

def calculate_personality_number(name: str) -> int:
    vowels = 'aeiou'
    consonants = [c for c in name.lower() if c.isalpha() and c not in vowels]
    total = sum(ord(c) - 96 for c in consonants)
    return reduce_to_core_number(total)

def get_life_path(day: int, month: int, year: int) -> int:
    digits = [int(d) for d in f"{day:02}{month:02}{year}"]
    total = sum(digits)
    return reduce_to_core_number(total)

def get_all_buttons(user_id, get_translation):
    return {
        "life_path": get_translation(user_id, "life_path"),
        "soul_urge": get_translation(user_id, "soul_urge"),
        "expression": get_translation(user_id, "expression"),
        "personality": get_translation(user_id, "personality"),
        "destiny": get_translation(user_id, "destiny"),
        "birthday_number": get_translation(user_id, "birthday_number"),
        "compatibility": get_translation(user_id, "compatibility"),
        "change_language": get_translation(user_id, "change_language"),
        "back_to_menu": get_translation(user_id, "back_to_menu"),
        "premium_tools": "💎 Premium Tools"
    }

from aiogram import types
from db import is_user_premium

async def handle_premium_lock(message: types.Message, user_id: int, lang: str, description: str) -> bool:
    if is_user_premium(user_id):
        return False  # User is premium — allow access

    premium_cta = {
        "en": "🔓 Unlock Premium",
        "lt": "🔓 Atrakinti Premium",
        "ru": "🔓 Разблокировать Премиум"
    }

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            premium_cta.get(lang, "🔓 Unlock Premium"),
            callback_data="simulate_premium_payment"
        )
    )

    await message.answer(
        f"{description}\n\n🔒 {get_translation(user_id, 'premium_tool_locked')}",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    return True  # Not premium — stop handler

def get_translation(user_id, key):
    lang = get_user_language(user_id)
    return translations.get(lang, translations['en']).get(key, key)


def main_menu_keyboard(user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)     
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "life_path")),
        types.KeyboardButton(get_translation(user_id, "soul_urge"))        
    )
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "expression")),
        types.KeyboardButton(get_translation(user_id, "personality"))                
    )
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "destiny")),
        types.KeyboardButton(get_translation(user_id, "birthday_number"))
    )
    keyboard.add(types.KeyboardButton(get_translation(user_id, "compatibility")))

    keyboard.add(types.KeyboardButton("💎 Premium Tools"))

    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "change_language")),
        types.KeyboardButton(get_translation(user_id, "back_to_menu"))
    )

    return keyboard
