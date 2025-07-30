from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from states import AngelNumberStates
from tools.premium_angel_number import get_angel_number_meaning
from handlers.common import main_menu
from handlers.common import is_premium_user


router = Router(name="premium_angel_number")


@router.message(StateFilter(AngelNumberStates.waiting_for_number))
async def handle_angel_number(message: Message, state: FSMContext):
    # 🔐 PREMIUM LOCK
    if not await is_premium_user(message.from_user.id):
        upgrade_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔓 Unlock Premium Now",
                    url="https://your-payment-link.com"  # ← replace with your payment link
                )]
            ]
        )
        await message.answer(
            "🚫 *This is a Premium Tool.*\n\nUnlock deeper guidance, karmic insights, and soul-aligned forecasts with *Futuredigits Premium* ✨",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=upgrade_button
        )
        return

    # ✅ PREMIUM USER CONTINUES
    try:
        number = message.text.strip()
        result = get_angel_number_meaning(number)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
        await state.clear()
    except Exception:
        await message.answer(
            "❗ *Invalid input.* Please enter a valid angel number, like `111` or `777`.",
            parse_mode=ParseMode.MARKDOWN
        )
