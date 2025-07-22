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
    await state.set_state(None)
    await message.answer(soul_urge_intro, reply_markup=main_menu)
    await state.set_state(SoulUrgeStates.waiting_for_full_name)

@router.message(F.state == SoulUrgeStates.waiting_for_full_name)
async def handle_name_for_soul_urge(message: Message, state: FSMContext):
    try:
        name = message.text.strip()
        print("[DEBUG] Name received:", name)  # 🟡 Add this line

        number = calculate_soul_urge_number(name)
        print("[DEBUG] Soul Urge Number:", number)  # 🟡 Add this line

        result = get_soul_urge_result(number)
        print("[DEBUG] Result length:", len(result))  # 🟡 Add this line

        await message.answer(result, reply_markup=main_menu)
        await state.clear()

    except Exception as e:
        print("[ERROR] Soul Urge Exception:", e)
        await message.answer(
            "❗ *Invalid input.* Please enter your full name.",
            parse_mode=ParseMode.MARKDOWN
        )

