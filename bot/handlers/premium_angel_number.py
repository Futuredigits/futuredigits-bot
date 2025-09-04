from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from localization import _, get_locale
from states import AngelNumberStates
from handlers.common import build_premium_menu
from tools.premium_angel_number import calculate_angel_key, get_angel_number_result

router = Router(name="angel_number")

@router.message(StateFilter(AngelNumberStates.waiting_for_number))
async def handle_angel_number(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        user_text = (message.text or "").strip()
        key = calculate_angel_key(user_text)
        result = get_angel_number_result(key, user_id=message.from_user.id, locale=loc)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_name", locale=loc), parse_mode=ParseMode.MARKDOWN)
