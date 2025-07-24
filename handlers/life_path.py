from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter  # ✅ Aiogram 3.x correct import
from aiogram.filters import StateFilter
from states import LifePathStates
from descriptions import life_path_intro
from tools.life_path import calculate_life_path_number, get_life_path_result
from handlers.common import main_menu

router = Router(name="life_path")

# ✅ 1) Menu button handler – always works, even if FSM active
@router.message(F.text == "🔢 Life Path", StateFilter("*"))
async def ask_birthdate_for_life_path(message: Message, state: FSMContext):
    await state.clear()  # reset any previous state
    await message.answer(
        life_path_intro,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu
    )
    await state.set_state(LifePathStates.waiting_for_birthdate)

# ✅ 2) FSM handler – ONLY listens in correct state
@router.message(StateFilter(LifePathStates.waiting_for_birthdate))
async def handle_birthdate_life_path(message: Message, state: FSMContext):
    print(f"[DEBUG] Life Path handler triggered, input: {message.text}")  # Debug log
    
    try:
        date_str = message.text.strip()
        number = calculate_life_path_number(date_str)
        print(f"[DEBUG] Calculated Life Path number: {number}")  # Debug log
        
        result = get_life_path_result(number)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.clear()  # clear after done
    
    except Exception:
        await message.answer(
            "❗ *Invalid date format.*\nPlease enter like this: `04.07.1992`",
            parse_mode=ParseMode.MARKDOWN
        )
