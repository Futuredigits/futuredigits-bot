
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import SoulUrgeStates
from descriptions import soul_urge_intro
from tools.soul_urge import calculate_soul_urge_number, get_soul_urge_result
from handlers.common import main_menu

router = Router(name="soul_urge")


@router.message(F.text == "💖 Soul Urge")
async def ask_full_name(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(soul_urge_intro, reply_markup=main_menu)
    await state.set_state(SoulUrgeStates.waiting_for_full_name)


@router.message(SoulUrgeStates.waiting_for_full_name)
async def handle_full_name(message: Message, state: FSMContext):
    try:
        name = message.text.strip()
        number = calculate_soul_urge_number(name)
        result = get_soul_urge_result(number)
        await message.answer(result, reply_markup=main_menu)
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter your full name as it appears on your birth certificate.",
            parse_mode=ParseMode.MARKDOWN
        )
