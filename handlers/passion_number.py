from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from states import PassionNumberStates
from descriptions import passion_intro
from tools.passion_number import calculate_passion_number, get_passion_result
from handlers.common import main_menu

router = Router(name="premium_passion")

@router.message(F.text == "🧩 Passion Number", StateFilter("*"))
async def ask_full_name_passion(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(passion_intro, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
    await state.set_state(PassionNumberStates.waiting_for_full_name)

@router.message(StateFilter(PassionNumberStates.waiting_for_full_name))
async def handle_passion_number(message: Message, state: FSMContext):
    try:
        full_name = message.text.strip()
        number = calculate_passion_number(full_name)
        result = get_passion_result(number)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.clear()
    except Exception:
        await message.answer("❗ *Invalid input.* Please enter your full name.", parse_mode=ParseMode.MARKDOWN)
