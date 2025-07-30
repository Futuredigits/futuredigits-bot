from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from bot import redis  # uses your existing Redis connection

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
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔢 Life Path"),
            KeyboardButton(text="💖 Soul Urge"),
            KeyboardButton(text="🎭 Personality"),
        ],
        [
            KeyboardButton(text="🎂 Birthday"),
            KeyboardButton(text="🎯 Expression"),
            KeyboardButton(text="🌟 Destiny"),
        ],
        [KeyboardButton(text="🔓 Premium Tools")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose a numerology tool...",
)

# ✅ Premium menu keyboard
premium_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧩 Passion Number"),
            KeyboardButton(text="🕳 Karmic Debt"),
            KeyboardButton(text="💑 Compatibility"),
        ],
        [
            KeyboardButton(text="❤️ Love Vibes"),
            KeyboardButton(text="🌌 Personal Year Forecast"),
            KeyboardButton(text="🌕 Moon Energy Today"),
        ],
        [
            KeyboardButton(text="🗓 Daily Universal Vibe"),
            KeyboardButton(text="🪬 Angel Number Decoder"),
            KeyboardButton(text="🌀 Name Vibration"),
        ],
        [KeyboardButton(text="🔙 Back to Main Menu")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Select a premium tool...",
)

# --- /start Command ---
@router.message(CommandStart(), StateFilter("*"))  # ✅ Always works
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=(
            "👋 *Welcome to Futuredigits!*\n\n"
            "We transform your birth date and name into deep numerological insights — calculated instantly.\n\n"
            "Discover your *Life Path*, *Soul Urge*, *Personality*, *Destiny* and more. "
            "Each tool gives you personalized meaning and clarity. 🌟\n\n"
            "Tap below to begin your numerology journey 🔮"
        ),
        reply_markup=main_menu,
        parse_mode=ParseMode.MARKDOWN,
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
        "💎 *Futuredigits Premium*\n\n"
        "Premium tools offer deeper readings, hidden number meanings, and exclusive interpretations.\n\n"
        "We are preparing full premium access. Stay tuned and explore what awaits. 🌟",
        parse_mode=ParseMode.MARKDOWN,
    )

# --- Premium menu ---
@router.message(F.text == "🔓 Premium Tools", StateFilter("*"))
async def show_premium_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "💎 *Premium Tools Menu*\n\nUnlock deeper insights, karmic secrets, and powerful relationship readings.",
        reply_markup=premium_menu,
        parse_mode=ParseMode.MARKDOWN,
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
    choice = message.text.strip()
    await state.clear()  # ✅ cancel any previous FSM

    if choice == "🔢 Life Path":
        await message.answer(life_path_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(LifePathStates.waiting_for_birthdate)

    elif choice == "💖 Soul Urge":
        await message.answer(soul_urge_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(SoulUrgeStates.waiting_for_full_name)

    elif choice == "🎭 Personality":
        await message.answer(personality_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(PersonalityStates.waiting_for_full_name)

    elif choice == "🎂 Birthday":
        await message.answer(birthday_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(BirthdayStates.waiting_for_birthdate)

    elif choice == "🎯 Expression":
        await message.answer(expression_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(ExpressionStates.waiting_for_full_name)

    elif choice == "🌟 Destiny":
        await message.answer(destiny_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
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
    choice = message.text.strip()
    await state.clear()

    if choice == "🧩 Passion Number":
        await message.answer(passion_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(PassionNumberStates.waiting_for_full_name)

    elif choice == "🕳 Karmic Debt":
        await message.answer(karmic_debt_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(KarmicDebtStates.waiting_for_birthdate)

    elif choice == "💑 Compatibility":
        await message.answer(compatibility_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(CompatibilityStates.waiting_for_two_names)

    elif choice == "❤️ Love Vibes":
        await message.answer(love_vibes_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(LoveVibesStates.waiting_for_full_name)

    elif choice == "🌌 Personal Year Forecast":
        await message.answer(personal_year_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.set_state(PersonalYearStates.waiting_for_birthdate)

    elif choice == "🌕 Moon Energy Today":
        from tools.premium_moon_energy import get_moon_energy_forecast
        result = get_moon_energy_forecast()
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)


    elif choice == "🗓 Daily Universal Vibe":
        from tools.premium_daily_vibe import get_daily_universal_vibe_forecast
        result = get_daily_universal_vibe_forecast()
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)


    elif choice == "🪬 Angel Number Decoder":
        await message.answer(
            angel_number_intro_premium,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu
        )
        await state.set_state(AngelNumberStates.waiting_for_number)


    elif choice == "🌀 Name Vibration":
        await message.answer(
            name_vibration_intro_premium,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu
        )
        await state.set_state(NameVibrationStates.waiting_for_full_name)

async def is_premium_user(user_id: int) -> bool:
    # Always allow YOU full access
    if user_id in {619941697}:
        return True

    value = await redis.get(f"user:{user_id}:premium")
    return value == b"1"


# --- Register this router ---
def register_common_handlers(dp):
    if router not in dp.sub_routers:
        dp.include_router(router)
