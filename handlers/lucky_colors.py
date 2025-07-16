from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import CareerProfileStates  # Reusing name input state
from db import get_user_language
from utils import get_translation, calculate_expression_number, handle_premium_lock, main_menu_keyboard

router = Router()

@router.message()
async def start_lucky_colors(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if message.text != get_translation(user_id, "lucky_colors_btn"):
        return

    locked = await handle_premium_lock(
        message,
        user_id,
        lang,
        description=get_translation(user_id, "lucky_colors")
    )
    if locked:
        return

    await message.answer(get_translation(user_id, "enter_full_name"))
    await state.set_state(CareerProfileStates.waiting_for_name)

@router.message(CareerProfileStates.waiting_for_name)
async def process_lucky_colors(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    number = calculate_expression_number(name)
    palette = {
        1: "🔴 Red, 🔵 Blue",
        2: "🟢 Green, 🤍 White",
        3: "🟡 Yellow, 🟣 Violet",
        4: "🟤 Brown, ⚫ Black",
        5: "🟠 Orange, 🟦 Aqua",
        6: "💖 Pink, 🤎 Earth tones",
        7: "🔵 Indigo, ⚪ Silver",
        8: "⚫ Black, 🔴 Burgundy",
        9: "🟣 Purple, 🤍 White"
    }

    colors = palette.get(number, "✨ Any color that uplifts your spirit")
    await message.answer(
        f"\U0001F3A8 *Lucky Colors & Numbers*\n\nYour number is {number}\nYour lucky colors: {colors}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()