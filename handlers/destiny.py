from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from states import DestinyStates
from descriptions import destiny_intro
from tools.destiny import calculate_destiny_number, get_destiny_result
from handlers.common import main_menu
import datetime

router = Router(name="destiny")

@router.message(F.text == "🌟 Destiny")
async def ask_destiny_input(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(destiny_intro, reply_markup=main_menu)
    await state.set_state(DestinyStates.waiting_for_birthdate_and_name)

@router.message(F.state == DestinyStates.waiting_for_birthdate_and_name)
async def handle_destiny(message: Message, state: FSMContext):
    try:
        raw = message.text.strip()
        *name_parts, date_str = raw.split()

        if not name_parts:
            raise ValueError("Missing name.")

        datetime.datetime.strptime(date_str, "%d.%m.%Y")

        name = " ".join(name_parts)
        number = calculate_destiny_number(name, date_str)
        result = get_destiny_result(number)

        await message.answer(result, reply_markup=main_menu)
        await state.clear()

    except Exception:
        await message.answer(
            "❗ *Invalid format.* Please send your full name followed by your birthdate:\n`Emma Grace 21.08.1992`",
            parse_mode=ParseMode.MARKDOWN
        )