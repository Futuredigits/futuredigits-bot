from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

# ✅ Import all required states for menu routing
from states import (
    LifePathStates,
    SoulUrgeStates,
    PersonalityStates,
    BirthdayStates,
    ExpressionStates,
    DestinyStates,
)

# ✅ Import all tool intro texts
from descriptions import (
    life_path_intro,
    soul_urge_intro,
    personality_intro,
    birthday_intro,
    expression_intro,
    destiny_intro,
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
        await message.answer(
            "🧩 *Passion Number*\n\n"
            "Discover the hidden longings and desires that move you deeply.\n\n"
            "👉 *Please enter your full name to calculate your Passion Number.*",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif choice == "🕳 Karmic Debt":
        await message.answer(
            "🕳 *Karmic Debt*\n\n"
            "Uncover karmic lessons from past lifetimes hidden in your birthdate.\n\n"
            "👉 *Please enter your birthdate in `DD.MM.YYYY` format.*",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif choice == "💑 Compatibility":
        await message.answer(
            "💑 *Compatibility Reading*\n\n"
            "See how two souls align through numerology.\n\n"
            "👉 *Please enter both full names separated by a comma.*\n"
            "`Example: Emma Grace, John Carter`",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif choice == "❤️ Love Vibes":
        await message.answer(
            "❤️ *Love Vibes Today*\n\n"
            "Find out today’s romantic numerology energy.\n\n"
            "👉 *Please enter your full name to receive your personalized reading.*",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif choice == "🌌 Personal Year Forecast":
        await message.answer(
            "🌌 *Personal Year Forecast*\n\n"
            "Discover the major numerology theme for your current personal year.\n\n"
            "👉 *Please enter your birthdate in `DD.MM.YYYY` format.*",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif choice == "🌕 Moon Energy Today":
        await message.answer(
            "🌕 *Moon Energy Today*\n\n"
            "Receive a numerology insight based on today’s lunar vibration. 🌙\n\n"
            "_No input needed – just tap this button again later for updated vibes._",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif choice == "🗓 Daily Universal Vibe":
        await message.answer(
            "🗓 *Daily Universal Vibe*\n\n"
            "See today’s universal numerology influence.\n\n"
            "_No input needed – just tap this button again later for updated vibes._",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif choice == "🪬 Angel Number Decoder":
        await message.answer(
            "🪬 *Angel Number Decoder*\n\n"
            "Enter the repeating number sequence you’ve been seeing (like `111`, `222`, `1234`).",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif choice == "🌀 Name Vibration":
        await message.answer(
            "🌀 *Name Vibration Analyzer*\n\n"
            "Enter any name (your own, a brand, or business) to see its energetic numerology signature.",
            parse_mode=ParseMode.MARKDOWN,
        )

# --- Register this router ---
def register_common_handlers(dp):
    if router not in dp.sub_routers:
        dp.include_router(router)
