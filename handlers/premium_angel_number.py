from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import AngelNumberStates
from handlers.common import build_premium_menu
from localization import _, get_locale
from tools.premium_angel_number import get_angel_number_result

router = Router(name="premium_angel_number")

@router.message(StateFilter(AngelNumberStates.waiting_for_sequence))
async def handle_angel_number(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        seq = (message.text or "").strip()
        result = get_angel_number_result(seq, user_id=message.from_user.id, locale=loc)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.clear()
    except Exception:
        # Same UX approach as your reference: gentle reprompt via i18n.
        await message.answer(_("angel_number_reprompt", locale=loc), parse_mode=ParseMode.MARKDOWN)
