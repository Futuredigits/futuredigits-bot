from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import NameVibrationStates
from tools.premium_name_vibration import get_name_vibration_meaning
from handlers.common import main_menu

router = Router(name="premium_name_vibration")

@router.message(StateFilter(NameVibrationStates.waiting_for_full_name))
async def handle_name_vibration(message: Message, state: FSMContext):
    try:
        full_name = message.text.strip()
        result = get_name_vibration_meaning(full_name)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter your full name.",
            parse_mode=ParseMode.MARKDOWN
        )
