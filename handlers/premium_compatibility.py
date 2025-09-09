from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import CompatibilityStates
from handlers.common import build_premium_menu
from localization import _, get_locale
from tools.premium_compatibility import calculate_compatibility, get_compatibility_result
from handlers.common import mark_activation_once

router = Router(name="premium_compatibility")

@router.message(StateFilter(CompatibilityStates.waiting_for_two_names))
async def handle_compatibility(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        raw = message.text.strip()
        if "," not in raw:
            raise ValueError("need two names")
        name1, name2 = [s.strip() for s in raw.split(",", 1)]
        if not name1 or not name2:
            raise ValueError("need two names")
        compat, score, n1, n2 = calculate_compatibility(name1, name2, locale=loc)
        result = get_compatibility_result(compat, score, user_id=message.from_user.id, locale=loc)

        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_two_names", locale=loc), parse_mode=ParseMode.MARKDOWN)
