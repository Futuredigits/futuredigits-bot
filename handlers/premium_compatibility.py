from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import CompatibilityStates
from tools.premium_compatibility import calculate_compatibility_score, get_compatibility_result
from handlers.common import premium_menu

router = Router(name="premium_compatibility")

@router.message(StateFilter(CompatibilityStates.waiting_for_two_names))
async def handle_compatibility(message: Message, state: FSMContext):
    try:
        raw = message.text.strip()
        if "," not in raw:
            raise ValueError("Missing comma")
        
        name1, name2 = [n.strip() for n in raw.split(",", 1)]
        if not name1 or not name2:
            raise ValueError("Both names required")

        # Calculate compatibility
        score = calculate_compatibility_score(name1, name2)
        result = get_compatibility_result(score, name1, name2)

        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
        await state.clear()

    except Exception:
        await message.answer(
            "❗ *Invalid format.* Please enter two full names separated by a comma:\n`Emma Grace, John Carter`",
            parse_mode=ParseMode.MARKDOWN
        )
