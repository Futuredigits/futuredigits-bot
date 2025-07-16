from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import CareerProfileStates  # Reusing same input state
from db import get_user_language
from utils import get_translation, calculate_soul_urge_number, handle_premium_lock, main_menu_keyboard

router = Router()

@router.message()
async def start_relationship_insights(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if message.text != get_translation(user_id, "relationship_insights_btn"):
        return

    locked = await handle_premium_lock(
        message,
        user_id,
        lang,
        description=get_translation(user_id, "relationship_insights")
    )
    if locked:
        return

    await message.answer(get_translation(user_id, "enter_full_name"))
    await state.set_state(CareerProfileStates.waiting_for_name)

@router.message(CareerProfileStates.waiting_for_name)
async def process_relationship_insights(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    number = calculate_soul_urge_number(name)
    key = f"soul_urge_description_{number}"
    description = get_translation(user_id, key)

    await message.answer(
        f"\U0001F497 *Love & Relationship Insight*\n\n{description}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()