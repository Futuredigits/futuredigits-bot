from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from states import LifePathStates
from descriptions import life_path_intro
from tools.life_path import calculate_life_path_number, get_life_path_result

router = Router(name=__name__)  # ✅ Unique router name

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔢 Life Path"), KeyboardButton(text="💖 Soul Urge"), KeyboardButton(text="🎭 Personality")],
        [KeyboardButton(text="🎂 Birthday"), KeyboardButton(text="🎯 Expression"), KeyboardButton(text="🌟 Destiny")],
        [KeyboardButton(text="🔓 Premium Tools")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose a numerology tool..."
)


premium_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧩 Passion Number"), KeyboardButton(text="🕳 Karmic Debt"), KeyboardButton(text="💑 Compatibility")],
        [KeyboardButton(text="❤️ Love Vibes"), KeyboardButton(text="🌌 Personal Year Forecast"), KeyboardButton(text="🌕 Moon Energy Today")],
        [KeyboardButton(text="🗓 Daily Universal Vibe"), KeyboardButton(text="🪬 Angel Number Decoder"), KeyboardButton(text="🌀 Name Vibration")],
        [KeyboardButton(text="🔙 Back to Main Menu")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Select a premium tool..."
)


# --- /start Command ---
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        text=(
            "👋 *Welcome to Futuredigits!*\n\n"
            "We transform your birth date and name into deep numerological insights — calculated instantly.\n\n"
            "Discover your *Life Path*, *Soul Urge*, *Personality*, *Destiny* and more. "
            "Each tool gives you personalized meaning and clarity. 🌟\n\n"
            "Tap below to begin your numerology journey 🔮"
        ),
        reply_markup=main_menu,
        parse_mode=ParseMode.MARKDOWN
    )

# --- /help Command ---
@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "🛠 *How to Use Futuredigits*\n\n"
        "Choose any numerology tool from the menu. You’ll be asked for your birth date or name.\n\n"
        "Each result is generated instantly with deep and professional insights. "
        "Want deeper results? Unlock *Premium Tools* 🎁",
        parse_mode=ParseMode.MARKDOWN
    )

# --- /premium Command ---
@router.message(Command("premium"))
async def premium_handler(message: Message):
    await message.answer(
        "💎 *Futuredigits Premium*\n\n"
        "Premium tools offer deeper readings, hidden number meanings, and exclusive interpretations.\n\n"
        "We are preparing full premium access. Stay tuned and explore what awaits. 🌟",
        parse_mode=ParseMode.MARKDOWN
    )


@router.message(F.text == "🔓 Premium Tools")
async def show_premium_menu(message: Message):
    await message.answer(
        "💎 *Premium Tools Menu*\n\nUnlock deeper insights, karmic secrets, and powerful relationship readings.",
        reply_markup=premium_menu,
        parse_mode=ParseMode.MARKDOWN
    )


@router.message(F.text == "🔙 Back to Main Menu")
async def show_main_menu(message: Message, state: FSMContext):
    await state.clear()  # ✅ clear any active tool state
    await message.answer(
        "🏠 *Back to Main Menu*\n\nChoose a numerology tool below to get started:",
        reply_markup=main_menu,
        parse_mode=ParseMode.MARKDOWN
    )



# --- Register this router once ---
def register_common_handlers(dp):
    if router not in dp.sub_routers:
        dp.include_router(router)
