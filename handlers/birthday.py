from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from states import BirthdayStates
from descriptions import birthday_intro
from tools.birthday import calculate_birthday_number, get_birthday_result
from handlers.common import main_menu

router = Router(name="birthday")


@router.message(StateFilter(BirthdayStates.waiting_for_birthdate))
async def handle_birthday(message: Message, state: FSMContext):
    try:
        date_str = message.text.strip()
        number = calculate_birthday_number(date_str)
        result = get_birthday_result(number)
        await message.answer(result, reply_markup=main_menu)
        await state.clear()
    except:
        await message.answer("❗ *Invalid date format.* Please use `DD.MM.YYYY`", parse_mode=ParseMode.MARKDOWN)