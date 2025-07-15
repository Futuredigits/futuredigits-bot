from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states import CompatibilityStates
from db import get_user_language
from utils import get_translation, is_valid_date, get_life_path, get_all_buttons

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "compatibility"))
async def start_compatibility(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    await message.answer(get_translation(user_id, "enter_first_birthdate_compatibility"))
    await CompatibilityStates.waiting_for_first_birthdate.set()

@dp.message_handler(state=CompatibilityStates.waiting_for_first_birthdate)
async def process_first_birthdate(message: types.Message, state: FSMContext):
    text = message.text.strip()
    user_id = message.from_user.id

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_date"))
        return

    await state.update_data(first_birthdate=text)
    await message.answer(get_translation(user_id, "enter_second_birthdate_compatibility"))
    await CompatibilityStates.waiting_for_second_birthdate.set()

@dp.message_handler(state=CompatibilityStates.waiting_for_second_birthdate)
async def process_second_birthdate(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    lang = get_user_language(user_id)

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_date"))
        return

    data = await state.get_data()
    first_birthdate = data.get("first_birthdate")

    day1, month1, year1 = map(int, first_birthdate.split('.'))
    day2, month2, year2 = map(int, text.split('.'))

    number1 = get_life_path(day1, month1, year1)
    number2 = get_life_path(day2, month2, year2)
    pair_key = f"{min(number1, number2)}_{max(number1, number2)}"
    description = get_translation(user_id, f"compatibility_{pair_key}")
    buttons = get_all_buttons(user_id, get_translation)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(buttons["life_path"], buttons["soul_urge"])
    keyboard.add(buttons["expression"], buttons["personality"])
    keyboard.add(buttons["destiny"], buttons["birthday_number"])
    keyboard.add(buttons["premium_tools"], buttons["change_language"])

    await message.answer(f"*{get_translation(user_id, 'compatibility_result')}*\n\n{description}",
                         parse_mode="Markdown", reply_markup=keyboard)
    await state.finish()
