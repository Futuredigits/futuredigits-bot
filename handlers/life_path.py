

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import LifePathStates
from descriptions import life_path_intro
from tools.life_path import calculate_life_path_number, get_life_path_result
from handlers.common import main_menu  # ✅ make sure main menu is still accessible

router = Router(name="life_path")


@router.message(F.text == "🔢 Life Path")
async def ask_birthdate_life_path(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(life_path_intro, reply_markup=main_menu)
    await state.set_state(LifePathStates.waiting_for_birthdate)


@router.message(LifePathStates.waiting_for_birthdate)
async def handle_birthdate_life_path(message: Message, state: FSMContext):
    try:
        date_str = message.text.strip()
        number = calculate_life_path_number(date_str)

        await message.answer(f"📅 You entered: `{date_str}`", parse_mode=ParseMode.MARKDOWN)
        await message.answer(f"🔢 Your Life Path Number is *{number}*", parse_mode=ParseMode.MARKDOWN)

        result = get_life_path_result(number)
        await message.answer(result, reply_markup=main_menu)

    except Exception:
        await message.answer(
            "❗ *Invalid date format.*\nPlease enter your birthdate in the format: `DD.MM.YYYY` 📅",
            parse_mode=ParseMode.MARKDOWN
        )
        return  # 🛑 Keep user in the same state to re-enter

    await state.clear()
