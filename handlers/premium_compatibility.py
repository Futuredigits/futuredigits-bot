from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import CompatibilityStates
from handlers.common import build_premium_menu
from localization import _, get_locale
from tools.premium_compatibility import calculate_compatibility, get_compatibility_result

router = Router(name="premium_compatibility")

@router.message(StateFilter(CompatibilityStates.waiting_for_two_birthdates))
async def handle_compatibility(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        date1, date2 = [d.strip() for d in message.text.strip().split()]
        number = calculate_compatibility(date1, date2)
        result = get_compatibility_result(number, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_two_dates", locale=loc), parse_mode=ParseMode.MARKDOWN)
