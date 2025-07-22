from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import PersonalityStates
from descriptions import personality_intro
from tools.personality import calculate_personality_number, get_personality_result
from handlers.common import main_menu

router = Router(name="personality")

@router.message(F.text == "🎭 Personality")
async def ask_name_for_personality(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(personality_intro, reply_markup=main_menu)
    await state.set_state(PersonalityStates.waiting_for_full_name)

@router.message(PersonalityStates.waiting_for_full_name)
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