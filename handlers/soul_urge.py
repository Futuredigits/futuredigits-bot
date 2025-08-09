from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from states import SoulUrgeStates
from descriptions import soul_urge_intro
from tools.soul_urge import calculate_soul_urge_number, get_soul_urge_result
from handlers.common import main_menu


router = Router(name="soul_urge")


@router.message(StateFilter(SoulUrgeStates.waiting_for_full_name))
async def handle_name_for_soul_urge(message: Message, state: FSMContext):
    print(f"[DEBUG] Soul Urge handler triggered, name: {message.text}")  # Debug log
    
    try:
        name = message.text.strip()
        number = calculate_soul_urge_number(name)
        print(f"[DEBUG] Soul Urge number: {number}")  # Debug log
        
        result = get_soul_urge_result(number)
        await message.answer(result, reply_markup=main_menu)
        await state.clear()
    
    except Exception as e:
        import traceback
        print("[ERROR] Soul Urge Exception:\n", traceback.format_exc())
        await message.answer(
            "❗ *Invalid input.* Please enter your full name.",
            parse_mode=ParseMode.MARKDOWN
        )


