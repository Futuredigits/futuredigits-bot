from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import DestinyStates
from handlers.common import build_main_menu
from handlers.common import mark_activation_once
from tools.profile_store import set_birthdate, set_full_name
from localization import _, get_locale
from tools.destiny import parse_name_and_birthdate, calculate_destiny_number, get_destiny_result

router = Router(name="destiny")

@router.message(StateFilter(DestinyStates.waiting_for_birthdate_and_name))
async def handle_destiny(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        full_name, date_str = parse_name_and_birthdate(message.text.strip())
        number = calculate_destiny_number(full_name, date_str, locale=loc)
        await set_full_name(message.from_user.id, full_name)
        await set_birthdate(message.from_user.id, date_str)
        result = get_destiny_result(number, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_date", locale=loc), parse_mode=ParseMode.MARKDOWN)
