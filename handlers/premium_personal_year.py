from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import PersonalYearStates
from tools.premium_personal_year import get_personal_year_forecast
from handlers.common import premium_menu

router = Router(name="premium_personal_year")

@router.message(StateFilter(PersonalYearStates.waiting_for_birthdate))
async def handle_personal_year(message: Message, state: FSMContext):
    try:
        birthdate = message.text.strip()
        result = get_personal_year_forecast(birthdate)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid date format.* Please use `DD.MM.YYYY`",
            parse_mode=ParseMode.MARKDOWN
        )
