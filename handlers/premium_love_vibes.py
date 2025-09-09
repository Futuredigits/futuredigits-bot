from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import LoveVibesStates
from handlers.common import build_premium_menu
from localization import _, get_locale
from tools.premium_love_vibes import calculate_love_vibe, get_love_vibes_result

router = Router(name="premium_love_vibes")

@router.message(StateFilter(LoveVibesStates.waiting_for_full_name))
async def handle_love_vibes(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        full_name = message.text.strip()
        number = calculate_love_vibe(full_name, locale=loc)
        result = get_love_vibes_result(number, user_id=message.from_user.id, locale=loc)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_name", locale=loc), parse_mode=ParseMode.MARKDOWN)
