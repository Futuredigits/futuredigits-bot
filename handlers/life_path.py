
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import LifePathStates
from utils import get_translation, is_valid_date, get_life_path, main_menu_keyboard
from db import get_user_language

router = Router()

@router.message(lambda message: message.text == get_translation(message.from_user.id, "life_path"))
async def start_life_path(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang_code = get_user_language(user_id)

    if lang_code == "lt":
        intro_text = (
            "🔢 *Gyvenimo Kelio Skaičius*
"
            "Tai svarbiausias skaičius jūsų numerologinėje analizėje.

"
            "Jis apskaičiuojamas pagal gimimo datą ir atskleidžia jūsų esmę, iššūkius bei likimą.

"
            "📅 Įveskite savo gimimo datą (DD.MM.YYYY):"
        )
    elif lang_code == "ru":
        intro_text = (
            "🔢 *Число Жизненного Пути*
"
            "Это главное число в вашей нумерологической карте.

"
            "Оно рассчитывается по дате рождения и показывает вашу суть, вызовы и судьбу.

"
            "📅 Введите дату рождения (ДД.ММ.ГГГГ):"
        )
    else:
        intro_text = (
            "🔢 *Life Path Number*
"
            "This number is the most important in your numerology chart.

"
            "It’s calculated from your birthdate and reveals your core personality, challenges, and destiny.

"
            "📅 Please enter your birthdate (DD.MM.YYYY):"
        )

    await state.set_state(LifePathStates.waiting_for_birthdate)
    await message.answer(intro_text, parse_mode="Markdown")

@router.message(LifePathStates.waiting_for_birthdate)
async def process_life_path_birthdate(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_format"))
        return

    day, month, year = map(int, text.split('.'))
    number = get_life_path(day, month, year)
    description = get_translation(user_id, f"life_path_description_{number}")
    title = get_translation(user_id, "life_path_result_title")

    response = f"💯 *{title} {number}*

{description}"
    await message.answer(response, parse_mode="Markdown")
    await message.answer(get_translation(user_id, "done_choose_tool"), reply_markup=main_menu_keyboard(user_id))
    await state.clear()
