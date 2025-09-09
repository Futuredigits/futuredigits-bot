from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import BirthdayStates
from tools.birthday import calculate_birthday_number, get_birthday_result
from handlers.common import build_main_menu
from localization import _, get_locale
from handlers.common import mark_activation_once


router = Router(name="birthday")

@router.message(StateFilter(BirthdayStates.waiting_for_birthdate))
async def handle_birthday(message: Message, state: FSMContext):
    try:
        loc = get_locale(message.from_user.id)
        date_str = message.text.strip()
        number = calculate_birthday_number(date_str)
        result = get_birthday_result(number, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_birthdate", locale=get_locale(message.from_user.id)), parse_mode=ParseMode.MARKDOWN)

