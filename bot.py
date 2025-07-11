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
from db import set_user_premium
from states import LuckyYearsStates
from db import is_user_premium
import datetime

import logging

def get_buttons(user_id):
    return {
        "life_path": get_translation(user_id, "life_path"),
        "soul_urge": get_translation(user_id, "soul_urge"),
        "expression": get_translation(user_id, "expression"),
        "personality": get_translation(user_id, "personality"),
        "destiny": get_translation(user_id, "destiny"),
        "birthday_number": get_translation(user_id, "birthday_number"),
        "compatibility": get_translation(user_id, "compatibility"),
        "change_language": get_translation(user_id, "change_language"),
        "back_to_menu": get_translation(user_id, "back_to_menu")
    }

def is_menu_command(text: str, user_id: int) -> bool:
    return text in get_buttons(user_id).values()
    
async def route_menu_command(message, state):
    text = message.text
    user_id = message.from_user.id
    if text == get_translation(user_id, "life_path"):
        return await handle_life_path(message, state)
    elif text == get_translation(user_id, "soul_urge"):
        return await start_soul_urge(message, state)
    elif text == get_translation(user_id, "expression"):
        return await start_expression(message, state)
    elif text == get_translation(user_id, "personality"):
        return await start_personality(message, state)
    elif text == get_translation(user_id, "destiny"):
        return await start_destiny(message, state)
    elif text == get_translation(user_id, "birthday_number"):
        return await start_birthday_number(message, state)
    elif text == get_translation(user_id, "compatibility"):
        return await start_compatibility(message, state)
    elif text == get_translation(user_id, "change_language"):
        return await prompt_language_change(message, state)
    elif text == get_translation(user_id, "back_to_menu"):
        return await back_to_main_menu(message, state)

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

       
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "life_path")),
        types.KeyboardButton(get_translation(user_id, "soul_urge")),
        types.KeyboardButton(get_translation(user_id, "expression"))
    )
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "personality")),
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

    # Inline "About" button
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("ℹ️ About", callback_data="about_info"))

    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
    await message.answer(get_translation(message.from_user.id, "done_choose_tool"), reply_markup=main_menu_keyboard(message.from_user.id))

@dp.callback_query_handler(lambda call: call.data == "about_info")
async def show_about_from_button(call: types.CallbackQuery):
    await call.message.answer(get_translation(call.from_user.id, "about"), parse_mode="Markdown")
    await call.answer()

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

@dp.message_handler(commands=["about"])
async def send_about(message: types.Message):
    text = get_translation(message.from_user.id, "about")
    await message.answer(text, parse_mode="Markdown")

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

@dp.message_handler(commands=["premium"])
async def send_premium_info(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    # Text block from translations.py
    text = get_translation(user_id, "premium_intro")

    # CTA button
    button_text = {
        "en": "🔓 Unlock Premium",
        "lt": "🔓 Atrakinti Premium",
        "ru": "🔓 Получить Premium"
    }

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        button_text.get(lang, button_text["en"]),
        callback_data="simulate_premium_payment"  # or "start_buy_premium"
    ))

    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)

@dp.message_handler(commands=["set_premium"])
async def make_user_premium(message: types.Message):
    set_user_premium(message.from_user.id, True)
    await message.answer("✅ You are now a premium user.")

@dp.message_handler(commands=["buy_premium"])
async def buy_premium(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    # Translated message
    text = {
        "en": (
            "💎 *FutureDigits Premium*\n\n"
            "Unlock all advanced numerology tools:\n"
            "• Lucky Years\n"
            "• Career Profile\n"
            "• Name Numerology\n"
            "• Love & Relationship Insights\n"
            "• Purpose & Mission Analysis\n\n"
            "💰 Price: *€9 one-time access*\n\n"
            "👉 This is a demo flow. Click below to simulate payment:"
        ),
        "lt": (
            "💎 *FutureDigits Premium*\n\n"
            "Atrakinkite visus pažangius numerologijos įrankius:\n"
            "• Sėkmingi Metai\n"
            "• Karjeros Profilis\n"
            "• Vardo Numerologija\n"
            "• Meilės ir Santykių Įžvalgos\n"
            "• Gyvenimo Paskirties Analizė\n\n"
            "💰 Kaina: *9 € vienkartinis mokestis*\n\n"
            "👉 Tai demonstracinė versija. Spauskite žemiau, kad imituotumėte mokėjimą:"
        ),
        "ru": (
            "💎 *FutureDigits Premium*\n\n"
            "Откройте все продвинутые нумерологические инструменты:\n"
            "• Удачные Годы\n"
            "• Карьерный Профиль\n"
            "• Нумерология Имени\n"
            "• Любовь и Отношения\n"
            "• Анализ Предназначения\n\n"
            "💰 Цена: *9 € однократный доступ*\n\n"
            "👉 Это демонстрация. Нажмите ниже, чтобы смоделировать оплату:"
        )
    }

    # Simulated "payment success" button
    button_text = {
        "en": "✅ Simulate Payment Success",
        "lt": "✅ Imituoti Sėkmingą Mokėjimą",
        "ru": "✅ Симулировать Успешную Оплату"
    }

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(button_text.get(lang, button_text["en"]), callback_data="simulate_premium_payment")
    )

    await message.answer(text.get(lang, text["en"]), reply_markup=keyboard, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == "💎 Premium Tools")
async def show_premium_menu(message: types.Message, state: FSMContext):  # <-- add state here
    await state.finish()  # ✅ cancel any previous input state

    user_id = message.from_user.id
    lang = get_user_language(user_id)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
async def handle_lucky_years(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if not is_user_premium(user_id):
        description = {
            "en": "📅 *Lucky Years Forecast*\nDiscover your most aligned years for success, transformation, and growth.",
            "lt": "📅 *Sėkmingų Metų Prognozė*\nSužinokite, kurie metai jums bus palankiausi sėkmei, pokyčiams ir augimui.",
            "ru": "📅 *Прогноз Удачных Лет*\nУзнайте, какие годы принесут вам успех, трансформацию и рост."
        }
        cta = {
            "en": "🔓 Unlock Premium",
            "lt": "🔓 Atrakinti Premium",
            "ru": "🔓 Получить Premium"
        }
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(cta.get(lang), callback_data="simulate_premium_payment"))
        await message.answer(description.get(lang) + "\n\n🔒 " + get_translation(user_id, "premium_tool_locked"),
                             parse_mode="Markdown", reply_markup=keyboard)
        return

    await message.answer(get_translation(user_id, "birthdate_prompt"), parse_mode="Markdown")
    await LuckyYearsStates.waiting_for_birthdate.set()

@dp.message_handler(state=LuckyYearsStates.waiting_for_birthdate)
async def process_lucky_years(message: types.Message, state: FSMContext):
    text = message.text.strip()
    user_id = message.from_user.id

    if is_menu_command(text, user_id):
        await state.finish()
        await route_menu_command(message, state)
        return

    try:
        day, month, year = map(int, text.split('.'))
        birth_year = int(year)
        lucky_years = [birth_year + 28, birth_year + 35, birth_year + 42]

        msg = {
            "en": f"📅 *Your Lucky Years*\nYour next aligned years for growth and transformation:\n\n🔹 {lucky_years[0]}, {lucky_years[1]}, {lucky_years[2]}",
            "lt": f"📅 *Jūsų Sėkmingi Metai*\nArtimiausi palankūs metai augimui ir proveržiui:\n\n🔹 {lucky_years[0]}, {lucky_years[1]}, {lucky_years[2]}",
            "ru": f"📅 *Ваши Удачные Годы*\nБлижайшие годы роста и трансформации:\n\n🔹 {lucky_years[0]}, {lucky_years[1]}, {lucky_years[2]}"
        }

        lang = get_user_language(user_id)
        await message.answer(msg.get(lang, msg["en"]), parse_mode="Markdown")
        await message.answer(get_translation(user_id, "premium_cta"), parse_mode="Markdown")
        await message.answer(get_translation(user_id, "done_choose_tool"), reply_markup=main_menu_keyboard(user_id))
        await state.finish()

    except:
        await message.answer(get_translation(user_id, "invalid_format"), parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "career_profile_btn"))
async def handle_career_profile(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if not is_user_premium(user_id):
        description = {
            "en": "💼 *Career Profile & Life Purpose*\nReveal your natural talents and how they align with your professional mission.",
            "lt": "💼 *Karjeros Profilis ir Paskirtis*\nSužinokite savo prigimtinius talentus ir jų ryšį su profesine misija.",
            "ru": "💼 *Карьерный Профиль и Предназначение*\nОткройте свои природные таланты и их связь с жизненным призванием."
        }
        cta = {
            "en": "🔓 Unlock Premium",
            "lt": "🔓 Atrakinti Premium",
            "ru": "🔓 Получить Premium"
        }
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(cta.get(lang), callback_data="simulate_premium_payment"))
        await message.answer(description.get(lang) + "\n\n🔒 " + get_translation(user_id, "premium_tool_locked"),
                             parse_mode="Markdown", reply_markup=keyboard)
        return

    explanations = {
        "en": "💼 *Career Profile & Life Purpose*\nEnter your birthdate (DD.MM.YYYY) to reveal your strongest career path based on your personal numerology.",
        "lt": "💼 *Karjeros Profilis ir Paskirtis*\nĮveskite savo gimimo datą (DD.MM.YYYY), kad sužinotumėte jums tinkamiausią profesinį kelią pagal numerologiją.",
        "ru": "💼 *Карьерный Профиль и Предназначение*\nВведите дату рождения (ДД.ММ.ГГГГ), чтобы узнать ваш наилучший карьерный путь по нумерологии."
    }

    await message.answer(explanations.get(lang, explanations["en"]), parse_mode="Markdown")
    await CareerProfileStates.waiting_for_birthdate.set()

@dp.message_handler(state=CareerProfileStates.waiting_for_birthdate)
async def process_career_profile(message: types.Message, state: FSMContext):
    text = message.text.strip()
    user_id = message.from_user.id

    if is_menu_command(text, user_id):
        await state.finish()
        await route_menu_command(message, state)
        return

    try:
        day, month, year = map(int, text.split('.'))
        total = sum(int(d) for d in f"{day:02}{month:02}{year}")
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(d) for d in str(total))

        career_map = {
            1: "Leadership, entrepreneurship, or pioneering roles suit you. You excel when creating your own path.",
            2: "You thrive in teamwork, diplomacy, and support roles. Careers in HR, counseling, or healing fit well.",
            3: "You shine in creative fields—media, writing, marketing, art. Communication is your strength.",
            4: "You’re reliable and structured. Engineering, planning, or technical work aligns with your nature.",
            5: "You need freedom and movement. Travel, sales, media, or innovation-driven roles suit you.",
            6: "You’re a nurturer and community builder. Careers in care, design, education, or family services align.",
            7: "You are analytical and introspective. Science, tech, psychology, or research is your zone.",
            8: "You’re built for leadership, business, finance, or management. Power and success motivate you.",
            9: "You’re idealistic and humanitarian. Nonprofit, art, healing, or mission-based work fulfills you.",
            11: "You’re a spiritual leader or visionary. Teaching, art, or guiding others is your path.",
            22: "You’re a master builder. Architecture, systems leadership, or social reform suit your vision.",
            33: "You’re a healer-teacher. Counseling, spiritual work, or emotional leadership is your highest path."
        }

        lang = get_user_language(user_id)
        summary = career_map.get(total, "Career insight not available.")
        title = {
            "en": f"💼 *Career Path: Number {total}*",
            "lt": f"💼 *Karjeros Kryptis: Skaičius {total}*",
            "ru": f"💼 *Карьера по Числу {total}*"
        }

        await message.answer(f"{title.get(lang, title['en'])}\n\n{summary}", parse_mode="Markdown")
        await message.answer(get_translation(user_id, "premium_cta"), parse_mode="Markdown")
        await message.answer(get_translation(user_id, "done_choose_tool"), reply_markup=main_menu_keyboard(user_id))
        await state.finish()

    except:
        await message.answer(get_translation(user_id, "invalid_format"), parse_mode="Markdown")



@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "name_numerology_btn"))
async def handle_name_numerology(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if not is_user_premium(user_id):
        description = {
            "en": "🧿 *Name Numerology*\nExplore the vibration of your name and how it influences your destiny.",
            "lt": "🧿 *Vardo Numerologija*\nSužinokite, kokią vibraciją skleidžia jūsų vardas ir kaip jis veikia jūsų kelią.",
            "ru": "🧿 *Нумерология Имени*\nУзнайте, как вибрация вашего имени влияет на вашу судьбу."
        }
        cta = {
            "en": "🔓 Unlock Premium",
            "lt": "🔓 Atrakinti Premium",
            "ru": "🔓 Получить Premium"
        }
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(cta.get(lang), callback_data="simulate_premium_payment"))
        await message.answer(description.get(lang) + "\n\n🔒 " + get_translation(user_id, "premium_tool_locked"),
                             parse_mode="Markdown", reply_markup=keyboard)
        return

    await message.answer(get_translation(user_id, "name_numerology"), parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "lucky_colors_btn"))
async def handle_lucky_colors(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if not is_user_premium(user_id):
        description = {
            "en": "🎨 *Lucky Colors & Numbers*\nDiscover the energies that enhance your personal magnetism and spiritual alignment.",
            "lt": "🎨 *Sėkmingos Spalvos ir Skaičiai*\nSužinokite, kokios energijos padeda jums pritraukti sėkmę ir vidinę harmoniją.",
            "ru": "🎨 *Счастливые Цвета и Числа*\nУзнайте, какие энергии усиливают вашу привлекательность и духовную гармонию."
        }
        cta = {
            "en": "🔓 Unlock Premium",
            "lt": "🔓 Atrakinti Premium",
            "ru": "🔓 Получить Premium"
        }
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(cta.get(lang), callback_data="simulate_premium_payment"))
        await message.answer(description.get(lang) + "\n\n🔒 " + get_translation(user_id, "premium_tool_locked"),
                             parse_mode="Markdown", reply_markup=keyboard)
        return

    await message.answer(get_translation(user_id, "lucky_colors"), parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "relationship_insights_btn"))
async def handle_relationship_insights(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if not is_user_premium(user_id):
        description = {
            "en": "💘 *Relationship Energy*\nUnderstand your emotional patterns and ideal romantic dynamics.",
            "lt": "💘 *Santykių Energija*\nSužinokite apie savo emocinius modelius ir idealų santykių ritmą.",
            "ru": "💘 *Энергия Отношений*\nПоймите свои эмоциональные паттерны и идеальные отношения."
        }
        cta = {
            "en": "🔓 Unlock Premium",
            "lt": "🔓 Atrakinti Premium",
            "ru": "🔓 Получить Premium"
        }
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(cta.get(lang), callback_data="simulate_premium_payment"))
        await message.answer(description.get(lang) + "\n\n🔒 " + get_translation(user_id, "premium_tool_locked"),
                             parse_mode="Markdown", reply_markup=keyboard)
        return

    await message.answer(get_translation(user_id, "relationship_insights"), parse_mode="Markdown")



@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "purpose_analysis_btn"))
async def handle_purpose_analysis(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if not is_user_premium(user_id):
        description = {
            "en": "🌟 *Life Purpose & Soul Mission*\nConnect with your higher calling and the lessons your soul came to learn.",
            "lt": "🌟 *Gyvenimo Paskirtis ir Sielos Misija*\nAtskleiskite savo aukštesnį tikslą ir pamokas, kurias siela atėjo patirti.",
            "ru": "🌟 *Предназначение и Миссия Души*\nПоймите своё призвание и уроки, с которыми пришла ваша душа."
        }
        cta = {
            "en": "🔓 Unlock Premium",
            "lt": "🔓 Atrakinti Premium",
            "ru": "🔓 Получить Premium"
        }
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(cta.get(lang), callback_data="simulate_premium_payment"))
        await message.answer(description.get(lang) + "\n\n🔒 " + get_translation(user_id, "premium_tool_locked"),
                             parse_mode="Markdown", reply_markup=keyboard)
        return

    await message.answer(get_translation(user_id, "purpose_analysis"), parse_mode="Markdown")



@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "detailed_compatibility_btn"))
async def handle_detailed_compatibility(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if not is_user_premium(user_id):
        description = {
            "en": "💑 *Detailed Compatibility*\nGo beyond life path numbers and explore deep soul-level connections.",
            "lt": "💑 *Išsamus Suderinamumas*\nSužinokite daugiau nei tik gyvenimo kelią – pažinkite gilesnius ryšius.",
            "ru": "💑 *Детальная Совместимость*\nИзучите глубинные связи на уровне душ, не только цифры путей жизни."
        }
        cta = {
            "en": "🔓 Unlock Premium",
            "lt": "🔓 Atrakinti Premium",
            "ru": "🔓 Получить Premium"
        }
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(cta.get(lang), callback_data="simulate_premium_payment"))

        await message.answer(
            description.get(lang) + "\n\n🔒 " + get_translation(user_id, "premium_tool_locked"),
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        return

    # TEMPORARY: Show description until logic is implemented
    await message.answer(
        "🛠️ Detailed Compatibility will compare multiple numerology numbers between you and your partner. Coming soon...",
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

    if is_menu_command(text, message.from_user.id):
        await state.finish()
        await route_menu_command(message, state)
        return
              
    vowels = 'aeiouAEIOU'
    total = sum(ord(c.lower()) - 96 for c in text if c.lower() in vowels and c.isalpha())
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))

    description_key = f"soul_urge_description_{total}"
    description = get_translation(message.from_user.id, description_key)
    title = get_translation(message.from_user.id, "soul_urge_result_title")

    await message.answer(f"{title} {total}\n\n{description}", parse_mode="Markdown")

    await message.answer(
        get_translation(message.from_user.id, "premium_cta"),
        parse_mode="Markdown"
    )

    await message.answer(
        get_translation(message.from_user.id, "done_choose_tool"),
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

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

    if is_menu_command(text, message.from_user.id):
        await state.finish()
        await route_menu_command(message, state)
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

    key = f"expression_description_{total}"
    description = get_translation(message.from_user.id, key)

    title = get_multilang_translation(message.from_user.id, "expression_result_title")

    await message.answer(f"{title} {total}\n\n{description}", parse_mode="Markdown")

    await message.answer(
        get_translation(message.from_user.id, "premium_cta"),
        parse_mode="Markdown"
    )

    await message.answer(
        get_translation(message.from_user.id, "done_choose_tool"),
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

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

    if is_menu_command(text, message.from_user.id):
        await state.finish()
        await route_menu_command(message, state)
        return
        
    vowels = 'aeiou'
    consonants = [c for c in text.lower() if c.isalpha() and c not in vowels]
    total = sum(ord(c) - 96 for c in consonants)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))

    description_key = f"personality_description_{total}"
    description = get_translation(message.from_user.id, description_key)
    title = get_translation(message.from_user.id, "personality_result_title")

    await message.answer(f"{title} {total}\n\n{description}", parse_mode="Markdown")

    await message.answer(
        get_translation(message.from_user.id, "premium_cta"),
        parse_mode="Markdown"
    )

    await message.answer(
        get_translation(message.from_user.id, "done_choose_tool"),
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

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

    if is_menu_command(text, message.from_user.id):
        await state.finish()
        await route_menu_command(message, state)
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

    await message.answer(f"{title} {total}\n\n{description}", parse_mode="Markdown")

    await message.answer(
        get_translation(message.from_user.id, "premium_cta"),
        parse_mode="Markdown"
    )

    await message.answer(
        get_translation(message.from_user.id, "done_choose_tool"),
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(message.from_user.id)
    )

    await state.finish()

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "birthday_number"), state="*")
async def start_birthday_number(message: types.Message, state: FSMContext):
    await state.finish()
    lang = get_user_language(message.from_user.id)

    explanations = {
        "en": "🎁 *Birthday Number*\nThis number reveals your unique gift and natural strength. It's calculated from the day you were born.\n\nEnter your birthdate (DD.MM.YYYY):",
        "lt": "🎁 *Gimimo Dienos Skaičius*\nŠis skaičius atskleidžia jūsų unikalią dovaną ir stiprybę. Jis skaičiuojamas pagal jūsų gimimo dieną.\n\nĮveskite gimimo datą (DD.MM.YYYY):",
        "ru": "🎁 *Число Дня Рождения*\nЭто число показывает ваш врожденный дар и силу. Оно берется из дня вашего рождения.\n\nВведите дату рождения (ДД.ММ.ГГГГ):"
    }

    await message.answer(explanations.get(lang, explanations["en"]), parse_mode="Markdown")
    await BirthdayStates.waiting_for_birthdate.set()

@dp.message_handler(state=BirthdayStates.waiting_for_birthdate)
async def process_birthday_number(message: types.Message, state: FSMContext):
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

    if is_menu_command(text, message.from_user.id):
        await state.finish()
        await route_menu_command(message, state)
        return
        
    try:
        day, month, year = map(int, text.split('.'))
        birthday_number = day
        while birthday_number > 9 and birthday_number not in [11, 22, 33]:
            birthday_number = sum(int(d) for d in str(birthday_number))

        title = get_translation(message.from_user.id, "birthday_result_title")
        description_key = f"birthday_description_{birthday_number}"
        description = get_translation(message.from_user.id, description_key)

        await message.answer(f"{title} {birthday_number}\n\n{description}", parse_mode="Markdown")
        await message.answer(get_translation(message.from_user.id, "premium_cta"), parse_mode="Markdown")
        await message.answer(get_translation(message.from_user.id, "done_choose_tool"), parse_mode="Markdown", reply_markup=main_menu_keyboard(message.from_user.id))
        await state.finish()

    except:
        await message.answer(get_translation(message.from_user.id, "invalid_format"), parse_mode="Markdown")

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

    if is_menu_command(text, message.from_user.id):
        await state.finish()
        await route_menu_command(message, state)
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

    if is_menu_command(text, message.from_user.id):
        await state.finish()
        await route_menu_command(message, state)
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


@dp.callback_query_handler(lambda call: call.data == "simulate_premium_payment")
async def handle_simulated_payment(call: types.CallbackQuery):
    user_id = call.from_user.id
    set_user_premium(user_id, True)

    confirmation = {
        "en": "🎉 *Payment successful!*\nYou now have full access to Premium tools.",
        "lt": "🎉 *Mokėjimas sėkmingas!*\nDabar turite prieigą prie visų Premium įrankių.",
        "ru": "🎉 *Оплата прошла успешно!*\nТеперь у вас есть доступ ко всем Premium инструментам."
    }

    await call.message.edit_reply_markup()  # remove button
    await call.message.answer(confirmation.get(get_user_language(user_id), confirmation["en"]), parse_mode="Markdown")


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

        await message.answer(f"{title} {life_path}\n\n{description}", parse_mode="Markdown")

        await message.answer(
            get_translation(user_id, "done_choose_tool"),
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(user_id)
        )

        await message.answer(
            get_translation(user_id, "premium_cta"),
            parse_mode="Markdown"
        )

    except:
        await message.answer(
            get_translation(message.from_user.id, "invalid_format"),
            parse_mode="Markdown"
        )

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

@app.on_event("shutdown")
async def on_shutdown():
    session = await bot.get_session()  # ✅ safe and async
    await session.close()
    logging.info("✅ Bot session closed safely")

@app.get("/")
async def health_check():
    return {"status": "ok"}
