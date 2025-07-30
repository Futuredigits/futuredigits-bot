from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import AngelNumberStates
from descriptions import angel_number_intro_premium
from handlers.common import main_menu, is_premium_user, get_upgrade_markup

router = Router(name="premium_angel_number")

# Triggered when user presses the "🪬 Angel Number Decoder" button
@router.message(StateFilter("*"))
async def angel_number_entry(message: Message, state: FSMContext):
    if message.text != "🪬 Angel Number Decoder":
        return

    if not await is_premium_user(message.from_user.id):
        await message.answer(
            "🚫 *This is a Premium Tool.*\n\n"
            "Unlock divine angel guidance, soul-level insights, and high-frequency forecasts with *Futuredigits Premium* 💎",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_upgrade_markup()
        )
        return

    # ✅ User is premium → show description + prompt
    await state.set_state(AngelNumberStates.waiting_for_number)
    await message.answer(
        angel_number_intro_premium,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu
    )


# Triggered when user enters a number (only for premium users)
@router.message(StateFilter(AngelNumberStates.waiting_for_number))
async def handle_angel_number(message: Message, state: FSMContext):
    from tools.premium_angel_number import get_angel_number_meaning

    try:
        number = message.text.strip()
        result = get_angel_number_meaning(number)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter a valid angel number, like `111`, `777`, or `1234`.",
            parse_mode=ParseMode.MARKDOWN
        )
