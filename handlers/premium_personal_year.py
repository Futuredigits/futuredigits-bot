from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import PersonalYearStates
from handlers.common import build_premium_menu
from localization import _, get_locale
from tools.premium_personal_year import calculate_personal_year, get_personal_year_result

router = Router(name="premium_personal_year")

@router.message(StateFilter(PersonalYearStates.waiting_for_birthdate))
async def handle_personal_year(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        date_str = message.text.strip()
        number = calculate_personal_year(date_str)
        result = get_personal_year_result(number, user_id=message.from_user.id, locale=loc)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_date", locale=loc), parse_mode=ParseMode.MARKDOWN)
