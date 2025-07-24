from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import AngelNumberStates
from descriptions import angel_number_intro
from tools.angel_numbers import decode_angel_number
from handlers.common import main_menu

router = Router(name="angel_numbers")

# Step 1: Intro & ask for number
@router.message(F.text == "🪬 Angel Number Decoder")
async def ask_angel_number(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(angel_number_intro, reply_markup=main_menu)
    await state.set_state(AngelNumberStates.waiting_for_angel_number)

# Step 2: Handle number
@router.message(AngelNumberStates.waiting_for_angel_number)
async def handle_angel_number(message: Message, state: FSMContext):
    try:
        num = message.text.strip()
        if not num.isdigit():
            raise ValueError("Not a valid number")
        
        meaning = decode_angel_number(num)
        await message.answer(meaning, reply_markup=main_menu)
        await state.clear()

    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter a number like `111`, `222`, or `1234`.",
            parse_mode="Markdown"
        )
