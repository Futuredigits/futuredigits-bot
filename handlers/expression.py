from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from states import ExpressionStates
from descriptions import expression_intro
from tools.expression import calculate_expression_number, get_expression_result
from handlers.common import main_menu

router = Router(name="expression")

@router.message(F.text == "🎯 Expression")
async def ask_expression_name(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(expression_intro, reply_markup=main_menu)
    await state.set_state(ExpressionStates.waiting_for_full_name)

@router.message(ExpressionStates.waiting_for_full_name)
async def handle_expression(message: Message, state: FSMContext):
    try:
        name = message.text.strip()
        number = calculate_expression_number(name)
        result = get_expression_result(number)
        await message.answer(result, reply_markup=main_menu)
        await state.clear()
    except:
        await message.answer("❗ *Invalid input.* Please enter your full name.", parse_mode=ParseMode.MARKDOWN)
