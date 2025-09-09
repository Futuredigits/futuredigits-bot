from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from localization import _, get_locale
from handlers.common import build_premium_menu
from states import NameVibrationStates
from tools.premium_name_vibration import calculate_name_vibration, get_name_vibration_result

router = Router(name="name_vibration")

@router.message(StateFilter(NameVibrationStates.waiting_for_full_name))
async def handle_name_vibration(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        full_name = (message.text or "").strip()
        number = calculate_name_vibration(full_name, locale=loc)
        result = get_name_vibration_result(number, user_id=message.from_user.id, locale=loc)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_name", locale=loc), parse_mode=ParseMode.MARKDOWN)
