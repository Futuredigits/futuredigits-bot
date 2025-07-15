from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import dp
from states import LifePathStates
from db import get_user_language
from utils import get_translation, is_valid_date, get_life_path, main_menu_keyboard

@dp.message_handler(state=None)
async def start_life_path(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text != get_translation(user_id, "life_path"):
        return

    await message.answer(get_translation(user_id, "birthdate_prompt"))
    await LifePathStates.waiting_for_birthdate.set()

@dp.message_handler(state=LifePathStates.waiting_for_birthdate)
async def process_life_path_birthdate(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_format"))
        return

    day, month, year = map(int, text.split('.'))
    number = get_life_path(day, month, year)
    description = get_translation(user_id, f"life_path_description_{number}")

    await message.answer(
        f"\U0001F4AF *{get_translation(user_id, 'life_path_result_title')} {number}*\n\n{description}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.finish()