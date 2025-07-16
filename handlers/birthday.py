from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import BirthdayStates
from db import get_user_language
from utils import get_translation, is_valid_date, main_menu_keyboard

router = Router()

@router.message(lambda message: message.text == get_translation(message.from_user.id, "birthday_number"))
async def start_birthday_number(message: types.Message, state: FSMContext):
    await message.answer(get_translation(message.from_user.id, "birthdate_prompt"))
    await state.set_state(BirthdayStates.waiting_for_birthdate)


@router.message(BirthdayStates.waiting_for_birthdate)
async def process_birthday_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_format"))
        return

    day = int(text.split('.')[0])
    number = day if day in [11, 22] or day < 10 else sum(map(int, str(day)))
    description = get_translation(user_id, f"birthday_description_{number}")

    await message.answer(
        f"\U0001F382 *{get_translation(user_id, 'birthday_result_title')} {number}*\n\n{description}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()