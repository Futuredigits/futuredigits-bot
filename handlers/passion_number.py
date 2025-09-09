from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import PassionNumberStates
from handlers.common import build_premium_menu
from localization import _, get_locale
from tools.premium_passion import calculate_passion_number, get_passion_number_result
from handlers.common import mark_activation_once


router = Router(name="passion_number")

@router.message(StateFilter(PassionNumberStates.waiting_for_full_name))
async def handle_passion_number(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        full_name = message.text.strip()
        number = calculate_passion_number(full_name, locale=loc)
        result = get_passion_number_result(number, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_name", locale=loc), parse_mode=ParseMode.MARKDOWN)
