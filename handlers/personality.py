from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import PersonalityStates
from handlers.common import build_main_menu
await set_full_name(message.from_user.id, full_name)
from localization import _, get_locale
from tools.personality import calculate_personality_number, get_personality_result
from handlers.common import mark_activation_once

router = Router(name="personality")

@router.message(StateFilter(PersonalityStates.waiting_for_full_name))
async def handle_personality(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        full_name = message.text.strip()
        number = calculate_personality_number(full_name, locale=loc)
        await set_full_name(message.from_user.id, full_name)
        result = get_personality_result(number, user_id=message.from_user.id)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await mark_activation_once(message.from_user.id)
        await state.clear()
    except Exception:
        await message.answer(_("error_invalid_name", locale=loc), parse_mode=ParseMode.MARKDOWN)
