from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import LifePathStates
from descriptions import life_path_intro
from tools.life_path import calculate_life_path_number, get_life_path_result
from handlers.common import main_menu

router = Router(name="life_path")


@router.message(F.text == "🔢 Life Path", state="*")
async def ask_birthdate_for_life_path(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        life_path_intro,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu
    )

    await state.set_state(LifePathStates.waiting_for_birthdate)


@router.message(LifePathStates.waiting_for_birthdate)
async def handle_birthdate_life_path(message: Message, state: FSMContext):
    print(f"[DEBUG] Life Path handler triggered, input: {message.text}")  # Debug log
    
    try:
        date_str = message.text.strip()
        number = calculate_life_path_number(date_str)
        print(f"[DEBUG] Calculated Life Path number: {number}")  # Debug log
        
        result = get_life_path_result(number)
        
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.clear()
    
    except Exception as e:
        import traceback
        print("[ERROR] Life Path exception:\n", traceback.format_exc())
        await message.answer(
            "❗ *Invalid date format.*\nPlease enter like this: `04.07.1992`",
            parse_mode=ParseMode.MARKDOWN
        )
