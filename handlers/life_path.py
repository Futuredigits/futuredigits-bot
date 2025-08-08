from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter  # ✅ Aiogram 3.x correct import

from states import LifePathStates
from tools.life_path import calculate_life_path_number, get_life_path_result
from handlers.common import get_main_menu


router = Router(name="life_path")

# ✅ FSM handler – ONLY listens when user is in LifePathStates.waiting_for_birthdate
@router.message(StateFilter(LifePathStates.waiting_for_birthdate))
async def handle_birthdate_life_path(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        date_str = message.text.strip()
        number = calculate_life_path_number(date_str)
        result = get_life_path_result(number, user_id)  # 👈 pass user_id
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu(user_id))
        await state.clear()

    except Exception:
        await message.answer(
            "❗ *Invalid date format.*\nPlease enter like this: `04.07.1992`",
            parse_mode=ParseMode.MARKDOWN
        )

