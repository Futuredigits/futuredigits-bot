from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states import ExpressionStates
from db import get_user_language
from utils import get_translation, calculate_expression_number, get_all_buttons

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "expression"))
async def start_expression(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    await message.answer(get_translation(user_id, "enter_full_name_expression"))
    await ExpressionStates.waiting_for_name.set()

@dp.message_handler(state=ExpressionStates.waiting_for_name)
async def process_expression_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()
    lang = get_user_language(user_id)

    number = calculate_expression_number(name)
    description = get_translation(user_id, f"expression_description_{number}")
    buttons = get_all_buttons(user_id, get_translation)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(buttons["life_path"], buttons["soul_urge"])
    keyboard.add(buttons["personality"], buttons["destiny"])
    keyboard.add(buttons["birthday_number"], buttons["compatibility"])
    keyboard.add(buttons["premium_tools"], buttons["change_language"])

    await message.answer(f"*{get_translation(user_id, 'expression_result')} {number}*\n\n{description}",
                         parse_mode="Markdown", reply_markup=keyboard)
    await state.finish()
