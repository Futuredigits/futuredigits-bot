from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from states import LifePathStates
from descriptions import life_path_intro
from tools.life_path import calculate_life_path_number, get_life_path_result

router = Router(name=__name__)  # ✅ Unique router name

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔢 Life Path"), KeyboardButton(text="💖 Soul Urge")],
        [KeyboardButton(text="🎭 Personality"), KeyboardButton(text="🔐 Birthday")],
        [KeyboardButton(text="🎯 Expression (Premium)"), KeyboardButton(text="🌟 Destiny (Premium)")],
        [KeyboardButton(text="🧩 Passion (Premium)"), KeyboardButton(text="🕳 Karmic Debt (Premium)")],
        [KeyboardButton(text="💑 Compatibility (Premium)"), KeyboardButton(text="❤️ Love Vibes (Premium)")],
        [KeyboardButton(text="🎁 Premium Tools")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose a numerology tool..."
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

# --- Life Path Number Tool ---
@router.message(F.text == "🔢 Life Path Number")
async def ask_birthdate_life_path(message: Message, state: FSMContext):
    await message.answer(life_path_intro, reply_markup=ReplyKeyboardRemove())
    await state.set_state(LifePathStates.waiting_for_birthdate)

@router.message(LifePathStates.waiting_for_birthdate)
async def handle_birthdate_life_path(message: Message, state: FSMContext):
    try:
        date_str = message.text.strip()
        number = calculate_life_path_number(date_str)
        result = get_life_path_result(number)
        await message.answer(result)
    except Exception:
        await message.answer("❗ Please enter a valid date in the format: YYYY-MM-DD")
    await state.clear()

# --- Register this router once ---
def register_common_handlers(dp):
    if router not in dp.sub_routers:
        dp.include_router(router)
