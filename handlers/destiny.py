from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import dp
from states import DestinyStates
from db import get_user_language
from utils import get_translation, calculate_destiny_number, get_all_buttons

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "destiny"))
async def start_destiny(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    await message.answer(get_translation(user_id, "enter_full_name_destiny"))
    await DestinyStates.waiting_for_name.set()

@dp.message_handler(state=DestinyStates.waiting_for_name)
async def process_destiny_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()
    lang = get_user_language(user_id)

    number = calculate_destiny_number(name)
    description = get_translation(user_id, f"destiny_description_{number}")
    buttons = get_all_buttons(user_id, get_translation)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(buttons["life_path"], buttons["soul_urge"])
    keyboard.add(buttons["expression"], buttons["personality"])
    keyboard.add(buttons["birthday_number"], buttons["compatibility"])
    keyboard.add(buttons["premium_tools"], buttons["change_language"])

    await message.answer(f"*{get_translation(user_id, 'destiny_result')} {number}*\n\n{description}",
                         parse_mode="Markdown", reply_markup=keyboard)
    await state.finish()
