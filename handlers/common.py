from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from localization import set_user_lang, get_text, get_main_menu
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F



# ✅ Replace with your actual Telegram user ID
OWNER_ID = 619941697

# Dummy database of paid users (in-memory for now)
PAID_USERS = set()

# Users who already used their 1-time free premium trial
USED_TRIAL = set()


def is_premium_user(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in PAID_USERS

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")
        ]
    ])


# ✅ Import all required states for menu routing
from states import (
    LifePathStates,
    SoulUrgeStates,
    PersonalityStates,
    BirthdayStates,
    ExpressionStates,
    DestinyStates,
    PassionNumberStates,
    KarmicDebtStates,
    CompatibilityStates,
    LoveVibesStates,
    PersonalYearStates,
    AngelNumberStates,
    NameVibrationStates,
)

from descriptions import (
    # Free tool intros
    life_path_intro,
    soul_urge_intro,
    personality_intro,
    birthday_intro,
    expression_intro,
    destiny_intro,

    # Premium tool intros
    passion_intro,
    karmic_debt_intro,
    compatibility_intro,
    love_vibes_intro,
    personal_year_intro,
    moon_energy_intro,
    daily_universal_vibe_intro,
    angel_number_intro_premium,
    name_vibration_intro_premium,
)

router = Router(name=__name__)  # ✅ Unique router name

# ✅ Main menu keyboard
def get_main_menu(user_id):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text("btn_life_path", user_id)),
                KeyboardButton(text=get_text("btn_soul_urge", user_id)),
                KeyboardButton(text=get_text("btn_personality", user_id)),
            ],
            [
                KeyboardButton(text=get_text("btn_birthday", user_id)),
                KeyboardButton(text=get_text("btn_expression", user_id)),
                KeyboardButton(text=get_text("btn_destiny", user_id)),
            ],
            [KeyboardButton(text=get_text("btn_premium", user_id))],
        ],
        resize_keyboard=True,
        input_field_placeholder=get_text("menu_main_placeholder", user_id),
    )


# ✅ Premium menu keyboard
def get_premium_menu(user_id):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text("btn_passion", user_id)),
                KeyboardButton(text=get_text("btn_karmic", user_id)),
                KeyboardButton(text=get_text("btn_compatibility", user_id)),
            ],
            [
                KeyboardButton(text=get_text("btn_love", user_id)),
                KeyboardButton(text=get_text("btn_personal_year", user_id)),
                KeyboardButton(text=get_text("btn_moon", user_id)),
            ],
            [
                KeyboardButton(text=get_text("btn_daily", user_id)),
                KeyboardButton(text=get_text("btn_angel", user_id)),
                KeyboardButton(text=get_text("btn_name_vibration", user_id)),
            ],
            [
                KeyboardButton(text=get_text("btn_upgrade", user_id)),
                KeyboardButton(text=get_text("btn_back", user_id)),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder=get_text("menu_premium_placeholder", user_id),
    )


# --- /start Command ---
@router.message(CommandStart(), StateFilter("*"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()

    # If user has no language yet → ask to choose
    user_id = message.from_user.id
    if get_user_lang(user_id) not in ["en", "ru"]:
        await message.answer(
            get_text("choose_language", user_id),
            reply_markup=get_language_keyboard()
        )
    else:
        await message.answer(
            get_text("start_message", user_id),
            reply_markup=get_main_menu(user_id),
            parse_mode=ParseMode.MARKDOWN
        )

@router.message(F.text.in_(["🇬🇧 English", "🇷🇺 Русский"]))
async def handle_language_choice(message: Message):
    user_id = message.from_user.id
    lang = "en" if message.text == "🇬🇧 English" else "ru"
    set_user_lang(user_id, lang)

    await message.answer(get_text(f"lang_set_{lang}", user_id))
    await message.answer(
        get_text("start_message", user_id),
        reply_markup=get_main_menu(user_id),
        parse_mode=ParseMode.MARKDOWN
    )


# --- /help Command ---
@router.message(Command("help"), StateFilter("*"))
async def help_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🛠 *How to Use Futuredigits*\n\n"
        "Choose any numerology tool from the menu. You’ll be asked for your birth date or name.\n\n"
        "Each result is generated instantly with deep and professional insights. "
        "Want deeper results? Unlock *Premium Tools* 🎁",
        parse_mode=ParseMode.MARKDOWN,
    )

# --- /premium Command ---
@router.message(Command("premium"), StateFilter("*"))
async def premium_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "💎 *Welcome to Futuredigits Premium*\n\n"
        "Unlock all advanced tools:\n"
        "🧩 Passion Number\n"
        "💑 Compatibility\n"
        "❤️ Love Vibes\n"
        "🕳 Karmic Debt\n"
        "🌌 Personal Year Forecast\n"
        "🌀 Name Energy & more...\n\n"
        "✨ *Benefits of Premium:*\n"
        "• Deeper forecasts (love, career, purpose)\n"
        "• Future timing and energy maps\n"
        "• Emotional insights, karmic patterns\n\n"
        "🔓 *Pricing Options:*\n"
        "• $7/week\n"
        "• $17/month\n"
        "• $79 lifetime (best value!)\n\n"
        "👉 [Click here to upgrade](https://your-payment-link.com)\n"
        "Then tap *Premium Tools* in the menu to explore.",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

@router.message(F.text == "💎 Upgrade Now", StateFilter("*"))
async def premium_cta_button(message: Message, state: FSMContext):
    # Just call the same handler as /premium
    await premium_handler(message, state)


# --- Premium menu ---
@router.message(F.text == "🔓 Premium Tools", StateFilter("*"))
async def show_premium_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "💎 *Premium Tools Menu*\n\n"
        "Unlock the hidden patterns of your *love life*, *past lives*, *soul purpose*, and *money energy*. 🔮\n\n"
        "✨ These exclusive tools offer deeper transformation and personal power.\n\n"
        "🎁 *You can try 1 Premium Tool for FREE!*\n"
        "Just tap any tool below to unlock your first insight.\n\n"
        "🚀 Want full access? [Upgrade Now](https://your-payment-link.com) to unlock everything instantly.",
        reply_markup=premium_menu,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )



@router.message(F.text == "🔙 Back to Main Menu", StateFilter("*"))
async def show_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 *Back to Main Menu*\n\nChoose a numerology tool below to get started:",
        reply_markup=main_menu,
        parse_mode=ParseMode.MARKDOWN,
    )

# ✅ Unified Main Menu Handler (handles all numerology tools)
@router.message(
    F.text.in_([
        "🔢 Life Path",
        "💖 Soul Urge",
        "🎭 Personality",
        "🎂 Birthday",
        "🎯 Expression",
        "🌟 Destiny",
    ]),
    StateFilter("*")  # ✅ Always works even if FSM active
)
async def unified_main_menu_handler(message: Message, state: FSMContext):
    """Single handler for all main menu tool buttons"""
    user_id = message.from_user.id
    choice = message.text.strip()
    await state.clear()  # ✅ cancel any previous FSM

    if choice == get_text("btn_life_path", user_id):
        await message.answer(get_text("intro_life_path", user_id), reply_markup=get_main_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(LifePathStates.waiting_for_birthdate)

    elif choice == get_text("btn_soul_urge", user_id):
        await message.answer(get_text("intro_soul_urge", user_id), reply_markup=get_main_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(SoulUrgeStates.waiting_for_full_name)

    elif choice == get_text("btn_personality", user_id):
        await message.answer(get_text("intro_personality", user_id), reply_markup=get_main_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(PersonalityStates.waiting_for_full_name)

    elif choice == get_text("btn_birthday", user_id):
        await message.answer(get_text("intro_birthday", user_id), reply_markup=get_main_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(BirthdayStates.waiting_for_birthdate)

    elif choice == get_text("btn_expression", user_id):
        await message.answer(get_text("intro_expression", user_id), reply_markup=get_main_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(ExpressionStates.waiting_for_full_name)

    elif choice == get_text("btn_destiny", user_id):
        await message.answer(get_text("intro_destiny", user_id), reply_markup=get_main_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(DestinyStates.waiting_for_birthdate_and_name)


# ✅ Unified Premium Menu Handler (only intros for now)
@router.message(
    F.text.in_([
        "🧩 Passion Number",
        "🕳 Karmic Debt",
        "💑 Compatibility",
        "❤️ Love Vibes",
        "🌌 Personal Year Forecast",
        "🌕 Moon Energy Today",
        "🗓 Daily Universal Vibe",
        "🪬 Angel Number Decoder",
        "🌀 Name Vibration",
    ]),
    StateFilter("*")
)
async def unified_premium_menu_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # 🔐 PREMIUM ACCESS CHECK
    if is_premium_user(user_id):
        pass

    elif user_id in USED_TRIAL:
        await state.clear()
        await message.answer(
            "🔒 *This is a Premium tool.*\n\n"
            "You've already used your 1 free premium tool trial. 💫\n\n"
            "To unlock all tools:\n"
            "💎 *$7/week* • *$17/month* • *$79 lifetime*\n\n"
            "👉 [Click here to upgrade](https://your-payment-link.com)\n"
            "Or tap *💎 Upgrade Now* below.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=premium_menu
        )
        return

    else:
        USED_TRIAL.add(user_id)
        await message.answer(
            "🎁 *You've unlocked a Premium tool for free!*\n\n"
            "Enjoy your reading — the next one will require an upgrade. 💎",
            parse_mode=ParseMode.MARKDOWN
        )

    choice = message.text.strip()
    await state.clear()

<<<<<<< HEAD
    if choice == "🧩 Passion Number":
        await message.answer(passion_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.set_state(PassionNumberStates.waiting_for_full_name)

    elif choice == "🕳 Karmic Debt":
        await message.answer(karmic_debt_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.set_state(KarmicDebtStates.waiting_for_birthdate)

    elif choice == "💑 Compatibility":
        await message.answer(compatibility_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.set_state(CompatibilityStates.waiting_for_two_names)

    elif choice == "❤️ Love Vibes":
        await message.answer(love_vibes_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.set_state(LoveVibesStates.waiting_for_full_name)

    elif choice == "🌌 Personal Year Forecast":
        await message.answer(personal_year_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
=======
    if choice == get_text("btn_passion", user_id):
        await message.answer(get_text("intro_passion", user_id), reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(PassionNumberStates.waiting_for_full_name)

    elif choice == get_text("btn_karmic", user_id):
        await message.answer(get_text("intro_karmic_debt", user_id), reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(KarmicDebtStates.waiting_for_birthdate)

    elif choice == get_text("btn_compatibility", user_id):
        await message.answer(get_text("intro_compatibility", user_id), reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(CompatibilityStates.waiting_for_two_names)

    elif choice == get_text("btn_love", user_id):
        await message.answer(get_text("intro_love_vibes", user_id), reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(LoveVibesStates.waiting_for_full_name)

    elif choice == get_text("btn_personal_year", user_id):
        await message.answer(get_text("intro_personal_year", user_id), reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)
>>>>>>> 27a53bf4df1a0b5419a4cdca2522c72e3e2ae32a
        await state.set_state(PersonalYearStates.waiting_for_birthdate)

    elif choice == get_text("btn_moon", user_id):
        from tools.premium_moon_energy import get_moon_energy_forecast
        result = get_moon_energy_forecast()
<<<<<<< HEAD
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
=======
        await message.answer(result, reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)
>>>>>>> 27a53bf4df1a0b5419a4cdca2522c72e3e2ae32a

    elif choice == get_text("btn_daily", user_id):
        from tools.premium_daily_vibe import get_daily_universal_vibe_forecast
        result = get_daily_universal_vibe_forecast()
<<<<<<< HEAD
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)

    elif choice == "🪬 Angel Number Decoder":
        await message.answer(angel_number_intro_premium, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.set_state(AngelNumberStates.waiting_for_number)

    elif choice == "🌀 Name Vibration":
        await message.answer(name_vibration_intro_premium, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
=======
        await message.answer(result, reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)

    elif choice == get_text("btn_angel", user_id):
        await message.answer(get_text("intro_angel_number", user_id), reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(AngelNumberStates.waiting_for_number)

    elif choice == get_text("btn_name_vibration", user_id):
        await message.answer(get_text("intro_name_vibration", user_id), reply_markup=get_premium_menu(user_id), parse_mode=ParseMode.MARKDOWN)
>>>>>>> 27a53bf4df1a0b5419a4cdca2522c72e3e2ae32a
        await state.set_state(NameVibrationStates.waiting_for_full_name)


# --- Register this router ---
def register_common_handlers(dp):
    if router not in dp.sub_routers:
        dp.include_router(router)
