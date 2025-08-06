from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import PassionNumberStates
from tools.premium_passion import calculate_passion_number, get_passion_number_result
from handlers.common import get_main_menu

router = Router(name="premium_passion")

@router.message(StateFilter(PassionNumberStates.waiting_for_full_name))
async def handle_passion_number(message: Message, state: FSMContext):
    try:
        full_name = message.text.strip()
        number = calculate_passion_number(full_name)
        result = get_passion_number_result(number)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu(user_id))
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter your full name.",
            parse_mode=ParseMode.MARKDOWN
        )
