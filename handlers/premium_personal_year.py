from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import PersonalYearStates
from tools.premium_personal_year import calculate_personal_year_number, get_personal_year_result
from handlers.common import main_menu

router = Router(name="premium_personal_year")

@router.message(StateFilter(PersonalYearStates.waiting_for_birthdate))
async def handle_personal_year(message: Message, state: FSMContext):
    try:
        birthdate = message.text.strip()
        year_number = calculate_personal_year_number(birthdate)
        result = get_personal_year_result(year_number)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.clear()

    except Exception:
        await message.answer(
            "❗ *Invalid date format.* Please use `DD.MM.YYYY`",
            parse_mode=ParseMode.MARKDOWN
        )
