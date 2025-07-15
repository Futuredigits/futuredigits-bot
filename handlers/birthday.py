from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states import BirthdayStates
from db import get_user_language
from utils import get_translation, is_valid_date, get_all_buttons

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "birthday_number"))
async def start_birthday_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    await message.answer(get_translation(user_id, "enter_birthdate_birthday"))
    await BirthdayStates.waiting_for_birthdate.set()

@dp.message_handler(state=BirthdayStates.waiting_for_birthdate)
async def process_birthday_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    lang = get_user_language(user_id)

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_date"))
        return

    day = int(text.split('.')[0])
    number = day if day < 10 or day in [11, 22] else sum(map(int, str(day)))
    description = get_translation(user_id, f"birthday_description_{number}")
    buttons = get_all_buttons(user_id, get_translation)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(buttons["life_path"], buttons["soul_urge"])
    keyboard.add(buttons["expression"], buttons["personality"])
    keyboard.add(buttons["destiny"], buttons["compatibility"])
    keyboard.add(buttons["premium_tools"], buttons["change_language"])

    await message.answer(f"*{get_translation(user_id, 'birthday_result')} {number}*\n\n{description}",
                         parse_mode="Markdown", reply_markup=keyboard)
    await state.finish()
