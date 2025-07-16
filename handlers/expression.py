from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import ExpressionStates
from db import get_user_language
from utils import get_translation, calculate_expression_number, main_menu_keyboard

router = Router()

@router.message(lambda message: message.text == get_translation(message.from_user.id, "expression"))
async def start_expression(message: types.Message, state: FSMContext):
    await message.answer(get_translation(message.from_user.id, "enter_full_name"))
    await state.set_state(ExpressionStates.waiting_for_name)

@router.message(ExpressionStates.waiting_for_name)
async def process_expression_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    number = calculate_expression_number(name)
    description = get_translation(user_id, f"expression_description_{number}")

    await message.answer(
        f"\U0001F9E0 *{get_translation(user_id, 'expression_result_title_en')} {number}*\n\n{description}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()