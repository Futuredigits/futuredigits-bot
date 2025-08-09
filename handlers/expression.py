from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from states import ExpressionStates
from descriptions import expression_intro
from tools.expression import calculate_expression_number, get_expression_result
from handlers.common import build_main_menu
from localization import _, get_locale

router = Router(name="expression")


@router.message(StateFilter(ExpressionStates.waiting_for_full_name))
async def handle_expression(message: Message, state: FSMContext):
    try:
        name = message.text.strip()
        number = calculate_expression_number(name)
        result = get_expression_result(number)
        await message.answer(result, reply_markup=main_menu)
        await state.clear()
    except:
        await message.answer("❗ *Invalid input.* Please enter your full name.", parse_mode=ParseMode.MARKDOWN)