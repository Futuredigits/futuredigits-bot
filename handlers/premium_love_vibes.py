from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import LoveVibesStates
from tools.premium_love_vibes import calculate_love_vibes, get_love_vibes_result
from handlers.common import build_premium_menu
from localization import _, get_locale

router = Router(name="premium_love_vibes")

@router.message(StateFilter(LoveVibesStates.waiting_for_full_name))
async def handle_love_vibes(message: Message, state: FSMContext):
    try:
        full_name = message.text.strip()
        score, vibe_number = calculate_love_vibes(full_name)
        result = get_love_vibes_result(full_name, score, vibe_number)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.clear()

    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter your full name.",
            parse_mode=ParseMode.MARKDOWN
        )
