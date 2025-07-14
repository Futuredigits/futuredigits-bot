import datetime

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

def get_all_buttons(translations, user_id, get_translation):
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
