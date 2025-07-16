from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import CompatibilityStates
from db import get_user_language
from utils import get_translation, is_valid_date, get_life_path, handle_premium_lock, main_menu_keyboard

router = Router()

@router.message()
async def start_detailed_compatibility(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if message.text != get_translation(user_id, "detailed_compatibility_btn"):
        return

    locked = await handle_premium_lock(
        message,
        user_id,
        lang,
        description=get_translation(user_id, "detailed_compatibility")
    )
    if locked:
        return

    await message.answer(get_translation(user_id, "enter_first_birthdate"))
    await state.set_state(CompatibilityStates.waiting_for_first_date)

@router.message(CompatibilityStates.waiting_for_first_date)
async def receive_first_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    date = message.text.strip()

    if not is_valid_date(date):
        await message.answer(get_translation(user_id, "invalid_format"))
        return

    await state.update_data(first_birthdate=date)
    await message.answer(get_translation(user_id, "enter_second_birthdate"))
    await state.set_state(CompatibilityStates.waiting_for_second_date)

@router.message(CompatibilityStates.waiting_for_second_date)
async def receive_second_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    date2 = message.text.strip()

    if not is_valid_date(date2):
        await message.answer(get_translation(user_id, "invalid_format"))
        return

    data = await state.get_data()
    date1 = data.get("first_birthdate")

    d1, m1, y1 = map(int, date1.split('.'))
    d2, m2, y2 = map(int, date2.split('.'))

    lp1 = get_life_path(d1, m1, y1)
    lp2 = get_life_path(d2, m2, y2)
    key = f"{min(lp1, lp2)}_{max(lp1, lp2)}"

    text = get_translation(user_id, f"compatibility_interpretation_{key}")
    await message.answer(
        f"\U0001F491 *Detailed Compatibility Report*\n\n{text}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()
