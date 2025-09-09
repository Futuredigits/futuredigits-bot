from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import KarmicDebtStates
from handlers.common import build_premium_menu
from localization import _, get_locale
from tools.premium_karmic_debt import calculate_karmic_debts, get_karmic_debt_result
from handlers.common import mark_activation_once

router = Router(name="premium_karmic_debt")

@router.message(StateFilter(KarmicDebtStates.waiting_for_birthdate))
async def handle_karmic_debt(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        date_str = message.text.strip()
        debts = calculate_karmic_debts(date_str)  # returns a sorted list: [13, 14] etc. or []
        result = get_karmic_debt_result(debts, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_date", locale=loc), parse_mode=ParseMode.MARKDOWN)
