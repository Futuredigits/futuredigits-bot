from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import KarmicDebtStates
from tools.premium_karmic_debt import calculate_karmic_debt_numbers, get_karmic_debt_result
from handlers.common import build_premium_menu
from localization import _, get_locale


router = Router(name="premium_karmic_debt")

@router.message(StateFilter(KarmicDebtStates.waiting_for_birthdate))
async def handle_karmic_debt(message: Message, state: FSMContext):
    try:
        date_str = message.text.strip()
        karmic_numbers = calculate_karmic_debt_numbers(date_str)
        result = get_karmic_debt_result(karmic_numbers)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid date format.* Please use `DD.MM.YYYY`",
            parse_mode=ParseMode.MARKDOWN
        )
