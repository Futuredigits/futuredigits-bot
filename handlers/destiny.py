from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import DestinyStates
from db import get_user_language
from utils import get_translation, calculate_expression_number, main_menu_keyboard

router = Router()

@router.message(lambda message: message.text == get_translation(message.from_user.id, "destiny"))
async def start_destiny(message: types.Message, state: FSMContext):
    await message.answer(get_translation(message.from_user.id, "enter_full_name"))
    await state.set_state(DestinyStates.waiting_for_name)


@router.message(DestinyStates.waiting_for_name)
async def process_destiny_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    # Destiny number = Expression number logic
    number = calculate_expression_number(name)
    description = get_translation(user_id, f"destiny_description_{number}")

    await message.answer(
        f"\U0001F31F *{get_translation(user_id, 'destiny_result_title')} {number}*\n\n{description}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()