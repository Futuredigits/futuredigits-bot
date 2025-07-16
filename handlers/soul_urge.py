from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import SoulUrgeStates
from db import get_user_language
from utils import get_translation, calculate_soul_urge_number, main_menu_keyboard

router = Router()

@router.message(lambda message: message.text == get_translation(message.from_user.id, "soul_urge"))
async def start_soul_urge(message: types.Message, state: FSMContext):
    await message.answer(get_translation(message.from_user.id, "enter_full_name"))
    await state.set_state(SoulUrgeStates.waiting_for_name)


@router.message(SoulUrgeStates.waiting_for_name)
async def process_soul_urge_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    number = calculate_soul_urge_number(name)
    description = get_translation(user_id, f"soul_urge_description_{number}")

    await message.answer(
        f"\U0001F496 *{get_translation(user_id, 'soul_urge_result_title')} {number}*\n\n{description}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()