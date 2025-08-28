from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import ExpressionStates
from handlers.common import build_main_menu
from localization import _, get_locale
from tools.expression import calculate_expression_number, get_expression_result

router = Router(name="expression")

@router.message(StateFilter(ExpressionStates.waiting_for_full_name))
async def handle_expression(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        full_name = message.text.strip()
        number = calculate_expression_number(full_name, locale=loc)
        result = get_expression_result(number, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_name", locale=loc), parse_mode=ParseMode.MARKDOWN)
