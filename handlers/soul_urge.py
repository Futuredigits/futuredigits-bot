from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import SoulUrgeStates
from handlers.common import build_main_menu
from localization import _, get_locale
from tools.soul_urge import calculate_soul_urge_number, get_soul_urge_result
from handlers.common import mark_activation_once


router = Router(name="soul_urge")

@router.message(StateFilter(SoulUrgeStates.waiting_for_full_name))
async def handle_soul_urge(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        full_name = message.text.strip()
        number = calculate_soul_urge_number(full_name, locale=loc)
        result = get_soul_urge_result(number, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_name", locale=loc), parse_mode=ParseMode.MARKDOWN)
