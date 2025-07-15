from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states import LifePathStates
from db import get_user_language
from utils import get_translation, is_valid_date, get_life_path, get_all_buttons

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "life_path"))
async def start_life_path(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    await message.answer(get_translation(user_id, "enter_birthdate_life_path"))
    await LifePathStates.waiting_for_birthdate.set()

@dp.message_handler(state=LifePathStates.waiting_for_birthdate)
async def process_life_path_birthdate(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    lang = get_user_language(user_id)

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_date"))
        return

    day, month, year = map(int, text.split('.'))
    number = get_life_path(day, month, year)
    description = get_translation(user_id, f"life_path_description_{number}")
    buttons = get_all_buttons(user_id, get_translation)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(buttons["soul_urge"], buttons["expression"])
    keyboard.add(buttons["personality"], buttons["destiny"])
    keyboard.add(buttons["birthday_number"], buttons["compatibility"])
    keyboard.add(buttons["premium_tools"], buttons["change_language"])

    await message.answer(f"*{get_translation(user_id, 'life_path_result')} {number}*\n\n{description}",
                         parse_mode="Markdown", reply_markup=keyboard)
    await state.finish()
