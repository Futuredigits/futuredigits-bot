from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import BirthdayStates
from tools.birthday import calculate_birthday_number, get_birthday_result
from handlers.common import build_main_menu
from localization import _, get_locale

router = Router(name="birthday")

@router.message(StateFilter(BirthdayStates.waiting_for_birthdate))
async def handle_birthday(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        date_str = message.text.strip()
        number = calculate_birthday_number(date_str)
        result = get_birthday_result(number)
        await message.answer(
            result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=build_main_menu(loc)
        )
        await state.clear()
    except Exception:
        await message.answer(
            _("err_invalid_date", locale=loc, example="04.07.1992"),
            parse_mode=ParseMode.MARKDOWN
        )
