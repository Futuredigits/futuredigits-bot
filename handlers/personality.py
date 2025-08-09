from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from states import PersonalityStates
from descriptions import personality_intro
from tools.personality import calculate_personality_number, get_personality_result
from handlers.common import build_main_menu
from localization import _, get_locale

router = Router(name="personality")


@router.message(StateFilter(PersonalityStates.waiting_for_full_name))
async def handle_name_for_personality(message: Message, state: FSMContext):
    try:
        name = message.text.strip()
        number = calculate_personality_number(name)
        result = get_personality_result(number)
        await message.answer(result, reply_markup=main_menu)
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter your full name.",
            parse_mode=ParseMode.MARKDOWN
        )