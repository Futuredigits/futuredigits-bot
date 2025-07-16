from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import LuckyYearsStates
from db import get_user_language
from utils import get_translation, is_valid_date, handle_premium_lock, main_menu_keyboard

router = Router()

@router.message()
async def start_lucky_years(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if message.text != get_translation(user_id, "lucky_years_btn"):
        return

    # Premium check
    locked = await handle_premium_lock(
        message,
        user_id,
        lang,
        description=get_translation(user_id, "lucky_years")
    )
    if locked:
        return

    await message.answer(get_translation(user_id, "birthdate_prompt"))
    await state.set_state(LuckyYearsStates.waiting_for_birthdate)

@router.message(LuckyYearsStates.waiting_for_birthdate)
async def process_lucky_years(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_format"))
        return

    day, month, year = map(int, text.split('.'))
    path = sum(map(int, f"{day:02}{month:02}{year}"))
    while path > 9:
        path = sum(int(d) for d in str(path))

    years = [year + i for i in range(1, 21) if (year + i) % path == 0]
    result = "\n".join(f"✅ {y}" for y in years[:10])

    await message.answer(
        f"\U0001F4C5 *Lucky Years (based on Life Path {path})*\n\n{result}",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user_id)
    )
    await state.clear()