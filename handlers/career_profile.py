from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import CareerProfileStates
from db import get_user_language
from utils import get_translation, calculate_expression_number, handle_premium_lock, main_menu_keyboard

router = Router()

@router.message()
async def start_career_profile(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if message.text != get_translation(user_id, "career_profile_btn"):
        return

    # Lock for non-premium
    locked = await handle_premium_lock(
        message,
        user_id,
        lang,
        description=get_translation(user_id, "career_profile")
    )
    if locked:
        return

    await message.answer(get_translation(user_id, "enter_full_name"))
    await state.set_state(CareerProfileStates.waiting_for_name)

@router.message(CareerProfileStates.waiting_for_name)
async def process_career_profile(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    number = calculate_expression_number(name)
    description = get_translation(user_id, f"expression_description_{number}")

    await message.answer(
        f"\U0001F4BC *Career Profile*\n\n{description}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()