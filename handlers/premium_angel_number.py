from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import AngelNumberStates
from tools.premium_angel_number import get_angel_number_meaning
from handlers.common import get_main_menu

router = Router(name="premium_angel_number")

@router.message(StateFilter(AngelNumberStates.waiting_for_number))
async def handle_angel_number(message: Message, state: FSMContext):
    try:
        number = message.text.strip()
        result = get_angel_number_meaning(number)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu(user_id))
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter a valid angel number, like `111` or `777`.",
            parse_mode=ParseMode.MARKDOWN
        )
