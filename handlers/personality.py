from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import PersonalityStates
from db import get_user_language
from utils import get_translation, calculate_personality_number, main_menu_keyboard

router = Router()

@router.message()
async def start_personality(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text != get_translation(user_id, "personality"):
        return

    await message.answer(get_translation(user_id, "enter_full_name"))
    await state.set_state(PersonalityStates.waiting_for_name)

@router.message(PersonalityStates.waiting_for_name)
async def process_personality_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    number = calculate_personality_number(name)
    description = get_translation(user_id, f"personality_description_{number}")

    await message.answer(
        f"\U0001F60E *{get_translation(user_id, 'personality_result_title')} {number}*\n\n{description}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()