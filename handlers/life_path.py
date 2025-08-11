from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import LifePathStates
from tools.life_path import calculate_life_path_number, get_life_path_result
from handlers.common import build_main_menu
from localization import _, get_locale

router = Router(name="life_path")

@router.message(StateFilter(LifePathStates.waiting_for_birthdate))
async def handle_life_path(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        date_str = message.text.strip()
        number = calculate_life_path_number(date_str)
        result = get_life_path_result(number, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_date", locale=loc), parse_mode=ParseMode.MARKDOWN)
