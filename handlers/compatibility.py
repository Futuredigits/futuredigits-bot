from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states import CompatibilityStates
from utils import get_translation, is_valid_date, get_life_path, main_menu_keyboard

router = Router()

@router.message(lambda message: message.text == get_translation(message.from_user.id, "compatibility"))
async def start_compatibility(message: types.Message, state: FSMContext):
    await message.answer(get_translation(message.from_user.id, "enter_first_birthdate"))
    await state.set_state(CompatibilityStates.waiting_for_first_date)


@router.message(CompatibilityStates.waiting_for_first_date)
async def get_first_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_format"))
        return

    await state.update_data(first_birthdate=text)
    await message.answer(get_translation(user_id, "enter_second_birthdate"))
    await state.set_state(CompatibilityStates.waiting_for_second_date)

@router.message(CompatibilityStates.waiting_for_second_date)
async def get_second_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    second = message.text.strip()

    if not is_valid_date(second):
        await message.answer(get_translation(user_id, "invalid_format"))
        return

    data = await state.get_data()
    first = data.get("first_birthdate")

    d1, m1, y1 = map(int, first.split('.'))
    d2, m2, y2 = map(int, second.split('.'))

    lp1 = get_life_path(d1, m1, y1)
    lp2 = get_life_path(d2, m2, y2)
    key = f"{min(lp1, lp2)}_{max(lp1, lp2)}"
    description = get_translation(user_id, f"compatibility_interpretation_{key}")

    await message.answer(
    f"\U0001F48F *{get_translation(user_id, 'compatibility')}*\n\n{description}",
    parse_mode="Markdown",
    reply_markup=main_menu_keyboard(user_id)
)

    await state.clear()