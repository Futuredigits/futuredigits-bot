import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from translations import translations
from db import set_user_language, get_user_language
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import CompatibilityStates
from states import SoulUrgeStates
from states import ExpressionStates
from states import PersonalityStates
from states import DestinyStates
from states import BirthdayStates

import logging

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
Bot.set_current(bot)  # 👈 this is required for webhook context
dp = Dispatcher(bot, storage=MemoryStorage())
Dispatcher.set_current(dp)  # 👈 this helps FSM handlers work properly

def compatibility_score(date1, date2):
    # Simple placeholder: compare Life Path Numbers
    def life_path(date_str):
        digits = [int(d) for d in date_str if d.isdigit()]
        total = sum(digits)
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(d) for d in str(total))
        return total

    n1 = life_path(date1)
    n2 = life_path(date2)
    diff = abs(n1 - n2)
    score = max(100 - diff * 10, 40)  # Just an example formula
    return score

def get_translation(user_id, key):
    lang = get_user_language(user_id)
    return translations.get(lang, translations['en']).get(key, key)

def get_multilang_translation(user_id, key):
    lang = get_user_language(user_id)
    value = translations.get(key)
    if isinstance(value, dict):
        return value.get(lang, value.get("en", ""))
    return value

soul_urge_descriptions = {
    1: "🔹 Independent Leader\nYou are driven by a desire to lead and make your mark. You thrive when you can act independently and inspire others through courage and determination.",
    2: "🔹 Peacemaker\nYour soul craves harmony, cooperation, and meaningful partnerships. You’re highly intuitive and sensitive to the needs of others.",
    3: "🔹 Creative Communicator\nYour inner self longs for expression through creativity, art, and joyful connection. You uplift those around you with your words and spirit.",
    4: "🔹 Steady Builder\nYou value stability, structure, and reliability. Deep inside, you yearn for a life built on discipline, hard work, and long-term security.",
    5: "🔹 Free Spirit\nYou crave freedom, adventure, and constant change. Your soul seeks variety, new experiences, and the thrill of exploration.",
    6: "🔹 Nurturer\nYour deepest desire is to care for others and create harmony at home and in relationships. Love, responsibility, and service are central to your path.",
    7: "🔹 Spiritual Seeker\nYou are drawn to introspection, wisdom, and deeper truths. Solitude and intellectual or spiritual exploration feed your soul.",
    8: "🔹 Ambitious Achiever\nYou’re internally motivated by success, power, and influence. Your soul’s path involves mastering the material world and leadership.",
    9: "🔹 Compassionate Humanitarian\nYou feel fulfilled by helping others and making the world a better place. Selflessness, empathy, and global awareness define your heart.",
    11: "🔹 Inspired Visionary (Master Number)\nYou have a powerful inner calling to inspire, uplift, and lead through spiritual or artistic channels. Your soul urges you to bring light to others.",
    22: "🔹 Master Builder (Master Number)\nYour destiny is tied to building great things for the collective. You crave creating systems or movements that leave a lasting impact.",
    33: "🔹 Master Teacher (Master Number)\nYou’re here to serve selflessly through love, healing, and compassion. Your soul calls you to uplift others through deep emotional wisdom."
}

# Keyboard with numerology options
def main_menu_keyboard(user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Free tools
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

    # Premium tools submenu
    keyboard.add(types.KeyboardButton("💎 Premium Tools"))

    # Settings
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "change_language")),
        types.KeyboardButton(get_translation(user_id, "back_to_menu"))
    )

    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    set_user_language(message.from_user.id, 'en')
    text = get_translation(message.from_user.id, "welcome")
    await message.answer(text, reply_markup=main_menu_keyboard(message.from_user.id))

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = (
        "📌 *FutureDigits Help Menu*\n\n"
        "Welcome! Here's what you can do:\n\n"
        "🔢 /start – Start the bot and choose your language\n"
        "🌟 Life Path, Soul Urge, Expression, Personality, Destiny, Birthday – Discover insights about yourself\n"
        "❤️ Compatibility – Compare two people by birthdates\n"
        "💎 Premium Tools – Explore advanced numerology tools (locked for now)\n"
        "🌍 /language – Change language (English, Lithuanian, Russian)\n\n"
        "If you need help at any time, just type /help ✨"
    )
    await message.answer(help_text, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "back_to_menu"), state="*")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔙 You are back in the main menu. Choose a tool below 👇", reply_markup=main_menu_keyboard(message.from_user.id))

@dp.message_handler(commands=['language'])
async def choose_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["English 🇬🇧", "Lietuvių 🇱🇹", "Русский 🇷🇺"]
    keyboard.add(*buttons)
    await message.answer("Choose your language / Pasirinkite kalbą / Выберите язык:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["English 🇬🇧", "Lietuvių 🇱🇹", "Русский 🇷🇺"], state="*")
async def set_language(message: types.Message, state: FSMContext):
    await state.finish()  # Cancel any ongoing input state
    lang_map = {
        "English 🇬🇧": "en",
        "Lietuvių 🇱🇹": "lt",
        "Русский 🇷🇺": "ru"
    }
    selected_lang = lang_map[message.text]
    set_user_language(message.from_user.id, selected_lang)
    await message.answer(get_translation(message.from_user.id, "language_set"), reply_markup=main_menu_keyboard(message.from_user.id))

@dp.message_handler(lambda message: message.text == "💎 Premium Tools")
async def show_premium_menu(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Premium tools grouped in rows
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "lucky_years_btn")),
        types.KeyboardButton(get_translation(user_id, "career_profile_btn"))
    )
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "name_numerology_btn")),
        types.KeyboardButton(get_translation(user_id, "lucky_colors_btn"))
    )
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "relationship_insights_btn")),
        types.KeyboardButton(get_translation(user_id, "purpose_analysis_btn"))
    )
    keyboard.add(types.KeyboardButton(get_translation(user_id, "detailed_compatibility_btn")))
    keyboard.add(types.KeyboardButton(get_translation(user_id, "back_to_menu")))

    descriptions = {
        "en": "💎 *Premium Tools*\nEnhance your life with advanced numerology insights. Choose a tool below 👇",
        "lt": "💎 *Premium Įrankiai*\nIšplėskite savo supratimą apie save naudodami pažangią numerologiją. Pasirinkite įrankį 👇",
        "ru": "💎 *Премиум Инструменты*\nУглубите понимание себя с помощью расширенной нумерологии. Выберите инструмент ниже 👇"
    }

    await message.answer(
        descriptions.get(lang, descriptions["en"]),
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "lucky_years_btn"))
async def handle_lucky_years(message: types.Message):
    description = get_translation(message.from_user.id, "lucky_years")
    locked_msg = get_translation(message.from_user.id, "premium_tool_locked")

    await message.answer(
        f"{description}\n\n🔒 {locked_msg}",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "career_profile_btn"))
async def handle_career_profile(message: types.Message):
    description = get_translation(message.from_user.id, "career_profile")
    locked_msg = get_translation(message.from_user.id, "premium_tool_locked")

    await message.answer(
        f"{description}\n\n🔒 {locked_msg}",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "name_numerology_btn"))
async def handle_name_numerology(message: types.Message):
    description = get_translation(message.from_user.id, "name_numerology")
    locked_msg = get_translation(message.from_user.id, "premium_tool_locked")

    await message.answer(
        f"{description}\n\n🔒 {locked_msg}",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "lucky_colors_btn"))
async def handle_lucky_colors(message: types.Message):
    description = get_translation(message.from_user.id, "lucky_colors")
    locked_msg = get_translation(message.from_user.id, "premium_tool_locked")

    await message.answer(
        f"{description}\n\n🔒 {locked_msg}",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "relationship_insights_btn"))
async def handle_relationship_insights(message: types.Message):
    description = get_translation(message.from_user.id, "relationship_insights")
    locked_msg = get_translation(message.from_user.id, "premium_tool_locked")

    await message.answer(
        f"{description}\n\n🔒 {locked_msg}",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "purpose_analysis_btn"))
async def handle_purpose_analysis(message: types.Message):
    description = get_translation(message.from_user.id, "purpose_analysis")
    locked_msg = get_translation(message.from_user.id, "premium_tool_locked")

    await message.answer(
        f"{description}\n\n🔒 {locked_msg}",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "detailed_compatibility_btn"))
async def handle_detailed_compatibility(message: types.Message):
    description = get_translation(message.from_user.id, "detailed_compatibility")
    locked_msg = get_translation(message.from_user.id, "premium_tool_locked")

    await message.answer(
        f"{description}\n\n🔒 {locked_msg}",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "life_path"), state=None)
async def handle_life_path(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    
    explanations = {
        "en": "✨ *Life Path Number*\nThis number reveals your core purpose, personality, and life direction. It’s calculated using your birthdate.\nLet’s find out what your life path is!",
        "lt": "✨ *Gyvenimo Kelio Skaičius*\nŠis skaičius atskleidžia jūsų gyvenimo tikslą, asmenybę ir kryptį. Jis skaičiuojamas pagal jūsų gimimo datą.\nSužinokime jūsų gyvenimo kelią!",
        "ru": "✨ *Число Жизненного Пути*\nЭто число раскрывает вашу основную цель, личность и направление в жизни. Оно рассчитывается по дате рождения.\nДавайте узнаем ваш путь!"
    }

    explanation = explanations.get(lang, explanations["en"])
    await message.answer(explanation, parse_mode="Markdown")
    await message.answer(get_translation(message.from_user.id, "birthdate_prompt"))

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, 'change_language'))
async def prompt_language_change(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["English 🇬🇧", "Lietuvių 🇱🇹", "Русский 🇷🇺"]
    keyboard.add(*buttons)
    await message.answer("Choose your language / Pasirinkite kalbą / Выберите язык:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "soul_urge"))
async def start_soul_urge(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)

    explanations = {
        "en": "💖 *Soul Urge Number*\nThis number reveals your inner desires, motivations, and what your heart truly longs for. It’s calculated using the vowels in your full name.\nNow, enter your full name 👇",
        "lt": "💖 *Sielos Troškimo Skaičius*\nŠis skaičius atskleidžia jūsų vidinius troškimus, motyvaciją ir tai, ko iš tikrųjų trokšta jūsų širdis. Jis skaičiuojamas pagal balses jūsų pilname varde.\nĮveskite savo pilną vardą 👇",
        "ru": "💖 *Число Душевного Стремления*\nЭто число раскрывает ваши внутренние желания, мотивацию и то, к чему стремится ваше сердце. Оно рассчитывается по гласным в полном имени.\nВведите ваше полное имя 👇"
    }

    explanation = explanations.get(lang, explanations["en"])
    await message.answer(explanation, parse_mode="Markdown")
    
    await SoulUrgeStates.waiting_for_name.set()

@dp.message_handler(state=SoulUrgeStates.waiting_for_name)
async def process_soul_urge(message: types.Message, state: FSMContext):
    text = message.text.strip()

    # List of all buttons (translated)
    buttons = {
        "life_path": get_translation(message.from_user.id, "life_path"),
        "soul_urge": get_translation(message.from_user.id, "soul_urge"),
        "expression": get_translation(message.from_user.id, "expression"),
        "personality": get_translation(message.from_user.id, "personality"),
        "destiny": get_translation(message.from_user.id, "destiny"),
        "birthday_number": get_translation(message.from_user.id, "birthday_number"),
        "compatibility": get_translation(message.from_user.id, "compatibility"),
        "change_language": get_translation(message.from_user.id, "change_language"),
        "back_to_menu": get_translation(message.from_user.id, "back_to_menu")
    }

    # If user pressed any other tool button — simulate that tool
    if text in buttons.values():
        await state.finish()

        # Forward user to the tool they selected
        if text == buttons["life_path"]:
            await handle_life_path(message, state)
        elif text == buttons["soul_urge"]:
            await start_soul_urge(message, state)
        elif text == buttons["expression"]:
            await start_expression(message, state)
        elif text == buttons["personality"]:
            await start_personality(message, state)
        elif text == buttons["destiny"]:
            await start_destiny(message, state)
        elif text == buttons["birthday_number"]:
            await start_birthday_number(message, state)
        elif text == buttons["compatibility"]:
            await start_compatibility(message, state)
        elif text == buttons["change_language"]:
            await prompt_language_change(message, state)
        elif text == buttons["back_to_menu"]:
            await back_to_main_menu(message, state)
        return

    # Otherwise — treat as a name and process Soul Urge logic
    vowels = 'aeiouAEIOU'
    total = sum(ord(c.lower()) - 96 for c in text if c.lower() in vowels and c.isalpha())
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))

    description_key = f"soul_urge_description_{total}"
    description = get_translation(message.from_user.id, description_key)
    title = get_translation(message.from_user.id, "soul_urge_result_title")

    await message.answer(f"{title} {total}\n\n{description}")
    await message.answer(get_translation(message.from_user.id, "done_choose_tool"), reply_markup=main_menu_keyboard(message.from_user.id))
    await state.finish()

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "expression"), state="*")
async def start_expression(message: types.Message, state: FSMContext):
    await state.finish()
    lang = get_user_language(message.from_user.id)

    explanations = {
        "en": "🔠 *Expression Number*\nThis number reveals your natural talents, abilities, and how you express yourself in the world. It’s calculated using all the letters in your full name.\nNow, enter your full name 👇",
        "lt": "🔠 *Išraiškos Skaičius*\nŠis skaičius atskleidžia jūsų natūralius talentus, gebėjimus ir tai, kaip save išreiškiate pasaulyje. Jis skaičiuojamas pagal visas raides jūsų pilname varde.\nĮveskite savo pilną vardą 👇",
        "ru": "🔠 *Число Самовыражения*\nЭто число показывает ваши природные таланты, способности и то, как вы проявляете себя в мире. Оно рассчитывается по всем буквам вашего полного имени.\nВведите ваше полное имя 👇"
    }

    explanation = explanations.get(lang, explanations["en"])
    await message.answer(explanation, parse_mode="Markdown")

    await ExpressionStates.waiting_for_name.set()

@dp.message_handler(state=ExpressionStates.waiting_for_name)
async def process_expression(message: types.Message, state: FSMContext):
    text = message.text.strip()
    buttons = {
        "life_path": get_translation(message.from_user.id, "life_path"),
        "soul_urge": get_translation(message.from_user.id, "soul_urge"),
        "expression": get_translation(message.from_user.id, "expression"),
        "personality": get_translation(message.from_user.id, "personality"),
        "destiny": get_translation(message.from_user.id, "destiny"),
        "birthday_number": get_translation(message.from_user.id, "birthday_number"),
        "compatibility": get_translation(message.from_user.id, "compatibility"),
        "change_language": get_translation(message.from_user.id, "change_language"),
        "back_to_menu": get_translation(message.from_user.id, "back_to_menu")
    }

    if text in buttons.values():
        await state.finish()
        if text == buttons["life_path"]:
            await handle_life_path(message, state)
        elif text == buttons["soul_urge"]:
            await start_soul_urge(message, state)
        elif text == buttons["expression"]:
            await start_expression(message, state)
        elif text == buttons["personality"]:
            await start_personality(message, state)
        elif text == buttons["destiny"]:
            await start_destiny(message, state)
        elif text == buttons["birthday_number"]:
            await start_birthday_number(message, state)
        elif text == buttons["compatibility"]:
            await start_compatibility(message, state)
        elif text == buttons["change_language"]:
            await prompt_language_change(message, state)
        elif text == buttons["back_to_menu"]:
            await back_to_main_menu(message, state)
        return

    # Calculate expression number
    name = text.lower()
    letter_map = {
        'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9,
        'j':1, 'k':2, 'l':3, 'm':4, 'n':5, 'o':6, 'p':7, 'q':8, 'r':9,
        's':1, 't':2, 'u':3, 'v':4, 'w':5, 'x':6, 'y':7, 'z':8
    }
    total = sum(letter_map.get(c, 0) for c in name if c.isalpha())
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))

    # Get translated description
    key = f"expression_description_{total}"
    description = get_translation(message.from_user.id, key)

    title = get_multilang_translation(message.from_user.id, "expression_result_title")
    await message.answer(f"{title} {total}\n\n{description}", parse_mode="Markdown")
    await message.answer(get_translation(message.from_user.id, "done_choose_tool"), reply_markup=main_menu_keyboard(message.from_user.id))
    await state.finish()

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "personality"), state="*")
async def start_personality(message: types.Message, state: FSMContext):
    await state.finish()
    lang = get_user_language(message.from_user.id)

    explanations = {
        "en": "😎 *Personality Number*\nThis number reveals how others perceive you — your outer personality and the impression you make. It’s calculated using the consonants in your full name.\nPlease enter your full name 👇",
        "lt": "😎 *Asmenybės Skaičius*\nŠis skaičius parodo, kaip jus mato kiti – jūsų išorinę asmenybę ir įspūdį, kurį paliekate. Jis skaičiuojamas pagal priebalses jūsų pilname varde.\nĮveskite savo pilną vardą 👇",
        "ru": "😎 *Число Личности*\nЭто число показывает, как вас воспринимают другие — вашу внешнюю личность и первое впечатление. Оно рассчитывается по согласным буквам вашего полного имени.\nВведите ваше полное имя 👇"
    }

    explanation = explanations.get(lang, explanations["en"])
    await message.answer(explanation, parse_mode="Markdown")
    await PersonalityStates.waiting_for_name.set()

@dp.message_handler(state=PersonalityStates.waiting_for_name)
async def process_personality(message: types.Message, state: FSMContext):
    text = message.text.strip()
    buttons = {
        "life_path": get_translation(message.from_user.id, "life_path"),
        "soul_urge": get_translation(message.from_user.id, "soul_urge"),
        "expression": get_translation(message.from_user.id, "expression"),
        "personality": get_translation(message.from_user.id, "personality"),
        "destiny": get_translation(message.from_user.id, "destiny"),
        "birthday_number": get_translation(message.from_user.id, "birthday_number"),
        "compatibility": get_translation(message.from_user.id, "compatibility"),
        "change_language": get_translation(message.from_user.id, "change_language"),
        "back_to_menu": get_translation(message.from_user.id, "back_to_menu")
    }

    if text in buttons.values():
        await state.finish()
        if text == buttons["life_path"]:
            await handle_life_path(message, state)
        elif text == buttons["soul_urge"]:
            await start_soul_urge(message, state)
        elif text == buttons["expression"]:
            await start_expression(message, state)
        elif text == buttons["personality"]:
            await start_personality(message, state)
        elif text == buttons["destiny"]:
            await start_destiny(message, state)
        elif text == buttons["birthday_number"]:
            await start_birthday_number(message, state)
        elif text == buttons["compatibility"]:
            await start_compatibility(message, state)
        elif text == buttons["change_language"]:
            await prompt_language_change(message, state)
        elif text == buttons["back_to_menu"]:
            await back_to_main_menu(message, state)
        return

    vowels = 'aeiou'
    consonants = [c for c in text.lower() if c.isalpha() and c not in vowels]
    total = sum(ord(c) - 96 for c in consonants)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))

    description_key = f"personality_description_{total}"
    description = get_translation(message.from_user.id, description_key)
    title = get_translation(message.from_user.id, "personality_result_title")

    await message.answer(f"{title} {total}\n\n{description}")
    await message.answer(get_translation(message.from_user.id, "done_choose_tool"), reply_markup=main_menu_keyboard(message.from_user.id))
    await state.finish()

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "destiny"), state="*")
async def start_destiny(message: types.Message, state: FSMContext):
    await state.finish()
    lang = get_user_language(message.from_user.id)

    explanations = {
        "en": "🌟 *Destiny Number*\nThis number reveals your life’s greater purpose, talents, and the path you're meant to fulfill. It’s calculated using all the letters in your full name.\nPlease enter your full name 👇",
        "lt": "🌟 *Likimo Skaičius*\nŠis skaičius atskleidžia jūsų gyvenimo paskirtį, talentus ir kelią, kuriuo turėtumėte eiti. Jis skaičiuojamas pagal visas raides jūsų pilname varde.\nĮveskite savo pilną vardą 👇",
        "ru": "🌟 *Число Судьбы*\nЭто число раскрывает ваше жизненное предназначение, таланты и путь, который вы должны пройти. Оно рассчитывается по всем буквам вашего полного имени.\nВведите ваше полное имя 👇"
    }

    explanation = explanations.get(lang, explanations["en"])
    await message.answer(explanation, parse_mode="Markdown")

    await DestinyStates.waiting_for_name.set()

@dp.message_handler(state=DestinyStates.waiting_for_name)
async def process_destiny(message: types.Message, state: FSMContext):
    text = message.text.strip()

    buttons = {
        "life_path": get_translation(message.from_user.id, "life_path"),
        "soul_urge": get_translation(message.from_user.id, "soul_urge"),
        "expression": get_translation(message.from_user.id, "expression"),
        "personality": get_translation(message.from_user.id, "personality"),
        "destiny": get_translation(message.from_user.id, "destiny"),
        "birthday_number": get_translation(message.from_user.id, "birthday_number"),
        "compatibility": get_translation(message.from_user.id, "compatibility"),
        "change_language": get_translation(message.from_user.id, "change_language"),
        "back_to_menu": get_translation(message.from_user.id, "back_to_menu")
    }

    if text in buttons.values():
        await state.finish()
        if text == buttons["life_path"]:
            await handle_life_path(message, state)
        elif text == buttons["soul_urge"]:
            await start_soul_urge(message, state)
        elif text == buttons["expression"]:
            await start_expression(message, state)
        elif text == buttons["personality"]:
            await start_personality(message, state)
        elif text == buttons["destiny"]:
            await start_destiny(message, state)
        elif text == buttons["birthday_number"]:
            await start_birthday_number(message, state)
        elif text == buttons["compatibility"]:
            await start_compatibility(message, state)
        elif text == buttons["change_language"]:
            await prompt_language_change(message, state)
        elif text == buttons["back_to_menu"]:
            await back_to_main_menu(message, state)
        return

    name = text.lower()
    letter_map = {
        'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9,
        'j':1, 'k':2, 'l':3, 'm':4, 'n':5, 'o':6, 'p':7, 'q':8, 'r':9,
        's':1, 't':2, 'u':3, 'v':4, 'w':5, 'x':6, 'y':7, 'z':8
    }
    total = sum(letter_map.get(c, 0) for c in name if c.isalpha())
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))

    title = get_multilang_translation(message.from_user.id, "destiny_result_title")
    description = get_translation(message.from_user.id, f"destiny_description_{total}")

    await message.answer(f"{title} {total}\n\n{description}")
    await message.answer(get_translation(message.from_user.id, "done_choose_tool"), reply_markup=main_menu_keyboard(message.from_user.id))
    await state.finish()

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "birthday_number"), state="*")
async def start_birthday_number(message: types.Message, state: FSMContext):
    await state.finish()
    lang = get_user_language(message.from_user.id)

    explanations = {
        "en": "🎂 *Birthday Number*\nThis number reveals a special talent or gift you were born with. It’s based solely on the day of the month you were born.\nPlease enter your birthdate in the format DD.MM.YYYY 👇",
        "lt": "🎂 *Gimtadienio Skaičius*\nŠis skaičius atskleidžia ypatingą talentą ar dovaną, su kuria gimėte. Jis grindžiamas tik jūsų gimimo mėnesio diena.\nĮveskite savo gimimo datą formatu DD.MM.YYYY 👇",
        "ru": "🎂 *Число Дня Рождения*\nЭто число раскрывает особый дар или талант, с которым вы родились. Оно основано только на дне вашего рождения.\nВведите свою дату рождения в формате DD.MM.YYYY 👇"
    }

    explanation = explanations.get(lang, explanations["en"])
    await message.answer(explanation, parse_mode="Markdown")

    await BirthdayStates.waiting_for_birthdate.set()

@dp.message_handler(state=BirthdayStates.waiting_for_birthdate)
async def process_birthday_number(message: types.Message, state: FSMContext):
    text = message.text.strip()

    # Redirect if a tool button is pressed
    buttons = {
        "life_path": get_translation(message.from_user.id, "life_path"),
        "soul_urge": get_translation(message.from_user.id, "soul_urge"),
        "expression": get_translation(message.from_user.id, "expression"),
        "personality": get_translation(message.from_user.id, "personality"),
        "destiny": get_translation(message.from_user.id, "destiny"),
        "birthday_number": get_translation(message.from_user.id, "birthday_number"),
        "compatibility": get_translation(message.from_user.id, "compatibility"),
        "change_language": get_translation(message.from_user.id, "change_language"),
        "back_to_menu": get_translation(message.from_user.id, "back_to_menu")
    }

    if text in buttons.values():
        await state.finish()
        if text == buttons["life_path"]:
            await handle_life_path(message, state)
        elif text == buttons["soul_urge"]:
            await start_soul_urge(message, state)
        elif text == buttons["expression"]:
            await start_expression(message, state)
        elif text == buttons["personality"]:
            await start_personality(message, state)
        elif text == buttons["destiny"]:
            await start_destiny(message, state)
        elif text == buttons["birthday_number"]:
            await start_birthday_number(message, state)
        elif text == buttons["compatibility"]:
            await start_compatibility(message, state)
        elif text == buttons["change_language"]:
            await prompt_language_change(message, state)
        elif text == buttons["back_to_menu"]:
            await back_to_main_menu(message, state)
        return

    # Process birthday number
    try:
        day, month, year = map(int, text.split('.'))
        birthday_number = day
        while birthday_number > 9 and birthday_number not in [11, 22, 33]:
            birthday_number = sum(int(d) for d in str(birthday_number))

        title = get_translation(message.from_user.id, "birthday_result_title")
        description_key = f"birthday_description_{birthday_number}"
        description = get_translation(message.from_user.id, description_key)

        await message.answer(f"{title} {birthday_number}\n\n{description}")
        await message.answer(get_translation(message.from_user.id, "done_choose_tool"), reply_markup=main_menu_keyboard(message.from_user.id))
        await state.finish()
    except:
        await message.answer(get_translation(message.from_user.id, "invalid_format"))

@dp.message_handler(lambda message: message.text == "❤️ Calculate Compatibility")
async def ask_birthdates_for_compatibility(message: types.Message):
    await message.answer("Please send two birthdates separated by a comma.\nExample: 14.05.1990, 22.09.1993")

    try:
        b1, b2 = [d.strip() for d in message.text.split(",")]
        day1, month1, year1 = map(int, b1.split('.'))
        day2, month2, year2 = map(int, b2.split('.'))

        def get_life_path(d, m, y):
            total = sum(int(d) for d in f"{d:02}{m:02}{y}")
            while total > 9 and total not in [11, 22, 33]:
                total = sum(int(x) for x in str(total))
            return total

        lp1 = get_life_path(day1, month1, year1)
        lp2 = get_life_path(day2, month2, year2)
        compatibility = 100 - abs(lp1 - lp2) * 10
        compatibility = max(0, min(compatibility, 100))

        # Determine meaning key based on score
        if compatibility >= 90:
            meaning_key = "compatibility_interpretation_90"
        elif compatibility >= 75:
            meaning_key = "compatibility_interpretation_75"
        elif compatibility >= 60:
            meaning_key = "compatibility_interpretation_60"
        elif compatibility >= 40:
            meaning_key = "compatibility_interpretation_40"
        else:
            meaning_key = "compatibility_interpretation_0"

        lang = get_user_language(message.from_user.id)
        desc1 = translations.get(lang, translations['en']).get(f"life_path_description_{lp1}", "")
        desc2 = translations.get(lang, translations['en']).get(f"life_path_description_{lp2}", "")
        title = translations.get(lang, translations['en']).get("life_path_result_title", "Life Path")
        meaning = get_translation(message.from_user.id, meaning_key)

        result = (
            f"{title} {lp1}\n🔹 {desc1}\n\n"
            f"{title} {lp2}\n🔹 {desc2}\n\n"
            f"❤️ Compatibility: {compatibility}%\n\n{meaning}"
        )

        await message.answer(result)

    except Exception as e:
        await message.answer("Invalid format. Please send two dates like this:\n`DD.MM.YYYY, DD.MM.YYYY`")

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "compatibility"), state="*")
async def start_compatibility(message: types.Message, state: FSMContext):
    await state.finish()
    lang = get_user_language(message.from_user.id)

    explanations = {
        "en": "💞 *Compatibility Analysis*\nCompare Life Path Numbers of two people. This reveals spiritual harmony and challenges.\nPlease enter the first person's birthdate (DD.MM.YYYY):",
        "lt": "💞 *Suderinamumo Analizė*\nPalyginkite dviejų žmonių gyvenimo kelius. Tai atskleidžia dvasinę darną ir iššūkius.\nĮveskite pirmojo asmens gimimo datą (DD.MM.YYYY):",
        "ru": "💞 *Анализ Совместимости*\nСравните Числа Жизненного Пути двух людей. Это покажет гармонию и вызовы.\nВведите дату рождения первого человека (ДД.ММ.ГГГГ):"
    }

    await message.answer(explanations.get(lang, explanations["en"]), parse_mode="Markdown")
    await CompatibilityStates.waiting_for_first_date.set()

@dp.message_handler(state=CompatibilityStates.waiting_for_first_date)
async def get_first_date(message: types.Message, state: FSMContext):
    text = message.text.strip()

    buttons = {
        "life_path": get_translation(message.from_user.id, "life_path"),
        "soul_urge": get_translation(message.from_user.id, "soul_urge"),
        "expression": get_translation(message.from_user.id, "expression"),
        "personality": get_translation(message.from_user.id, "personality"),
        "destiny": get_translation(message.from_user.id, "destiny"),
        "birthday_number": get_translation(message.from_user.id, "birthday_number"),
        "compatibility": get_translation(message.from_user.id, "compatibility"),
        "change_language": get_translation(message.from_user.id, "change_language"),
        "back_to_menu": get_translation(message.from_user.id, "back_to_menu")
    }

    if text in buttons.values():
        await state.finish()
        if text == buttons["life_path"]:
            await handle_life_path(message, state)
        elif text == buttons["soul_urge"]:
            await start_soul_urge(message, state)
        elif text == buttons["expression"]:
            await start_expression(message, state)
        elif text == buttons["personality"]:
            await start_personality(message, state)
        elif text == buttons["destiny"]:
            await start_destiny(message, state)
        elif text == buttons["birthday_number"]:
            await start_birthday_number(message, state)
        elif text == buttons["compatibility"]:
            await start_compatibility(message, state)
        elif text == buttons["change_language"]:
            await prompt_language_change(message, state)
        elif text == buttons["back_to_menu"]:
            await back_to_main_menu(message, state)
        return

    try:
        day, month, year = map(int, text.split('.'))
        await state.update_data(first_date=text)  # ✅ Essential line
        await CompatibilityStates.next()
        await message.answer("Now enter the second birthdate (DD.MM.YYYY):")
    except:
        await message.answer("❌ Invalid date format. Please use DD.MM.YYYY.")

@dp.message_handler(state=CompatibilityStates.waiting_for_second_date)
async def get_second_date(message: types.Message, state: FSMContext):
    text = message.text.strip()

    buttons = {
        "life_path": get_translation(message.from_user.id, "life_path"),
        "soul_urge": get_translation(message.from_user.id, "soul_urge"),
        "expression": get_translation(message.from_user.id, "expression"),
        "personality": get_translation(message.from_user.id, "personality"),
        "destiny": get_translation(message.from_user.id, "destiny"),
        "birthday_number": get_translation(message.from_user.id, "birthday_number"),
        "compatibility": get_translation(message.from_user.id, "compatibility"),
        "change_language": get_translation(message.from_user.id, "change_language"),
        "back_to_menu": get_translation(message.from_user.id, "back_to_menu")
    }

    if text in buttons.values():
        await state.finish()
        if text == buttons["life_path"]:
            await handle_life_path(message, state)
        elif text == buttons["soul_urge"]:
            await start_soul_urge(message, state)
        elif text == buttons["expression"]:
            await start_expression(message, state)
        elif text == buttons["personality"]:
            await start_personality(message, state)
        elif text == buttons["destiny"]:
            await start_destiny(message, state)
        elif text == buttons["birthday_number"]:
            await start_birthday_number(message, state)
        elif text == buttons["compatibility"]:
            await start_compatibility(message, state)
        elif text == buttons["change_language"]:
            await prompt_language_change(message, state)
        elif text == buttons["back_to_menu"]:
            await back_to_main_menu(message, state)
        return

    try:
        day2, month2, year2 = map(int, text.split('.'))
        data = await state.get_data()
        first_date = data.get("first_date")

        if not first_date:
            await message.answer("⚠️ First birthdate is missing. Please start again.")
            await start_compatibility(message, state)
            return

        day1, month1, year1 = map(int, first_date.split('.'))

        def get_life_path(d, m, y):
            total = sum(int(d) for d in f"{d:02}{m:02}{y}")
            while total > 9 and total not in [11, 22, 33]:
                total = sum(int(x) for x in str(total))
            return total

        lp1 = get_life_path(day1, month1, year1)
        lp2 = get_life_path(day2, month2, year2)
        compatibility = 100 - abs(lp1 - lp2) * 10
        compatibility = max(0, min(compatibility, 100))

        # Determine meaning key
        if compatibility >= 90:
            meaning_key = "compatibility_interpretation_90"
        elif compatibility >= 75:
            meaning_key = "compatibility_interpretation_75"
        elif compatibility >= 60:
            meaning_key = "compatibility_interpretation_60"
        elif compatibility >= 40:
            meaning_key = "compatibility_interpretation_40"
        else:
            meaning_key = "compatibility_interpretation_0"

        lang = get_user_language(message.from_user.id)
        desc1 = translations.get(lang, translations['en']).get(f"life_path_description_{lp1}", "")
        desc2 = translations.get(lang, translations['en']).get(f"life_path_description_{lp2}", "")
        title = translations.get(lang, translations['en']).get("life_path_result_title", "Life Path")
        meaning = get_translation(message.from_user.id, meaning_key)

        result = (
            f"{title} {lp1}\n🔹 {desc1}\n\n"
            f"{title} {lp2}\n🔹 {desc2}\n\n"
            f"❤️ Compatibility: {compatibility}%\n\n{meaning}"
        )

        await message.answer(result, parse_mode="Markdown")
        await message.answer(get_translation(message.from_user.id, "done_choose_tool"), reply_markup=main_menu_keyboard(message.from_user.id))
        await state.finish()

    except:
        await message.answer("❌ Invalid date format. Please use DD.MM.YYYY.")

@dp.message_handler()
async def handle_all_inputs(message: types.Message):
    try:
        day, month, year = map(int, message.text.strip().split('.'))
        life_path = sum(int(digit) for digit in f"{day:02}{month:02}{year}")
        while life_path > 9 and life_path not in [11, 22, 33]:
            life_path = sum(int(d) for d in str(life_path))

        user_id = message.from_user.id
        title = get_translation(user_id, "life_path_result_title")
        description = get_translation(user_id, f"life_path_description_{life_path}")

        await message.answer(
            f"{title} {life_path}\n\n{description}",
            parse_mode="Markdown"
        )
        await message.answer(
            get_translation(user_id, "done_choose_tool"),
            reply_markup=main_menu_keyboard(user_id)
        )

    except:
        await message.answer(get_translation(message.from_user.id, "invalid_format"))

from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    webhook_url = f"{os.getenv('WEBHOOK_BASE')}/webhook/{os.getenv('BOT_TOKEN')}"
    await bot.set_webhook(webhook_url)
    logging.info(f"✅ Webhook set to: {webhook_url}")

@app.post("/webhook/{token}")
async def telegram_webhook(token: str, request: Request):
    if token != os.getenv("BOT_TOKEN"):
        return {"error": "Invalid token"}
    update = await request.json()
    telegram_update = types.Update(**update)
    await dp.process_update(telegram_update)
    return {"status": "ok"}

