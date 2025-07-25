from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from tools.premium_daily_vibe import get_daily_universal_vibe_forecast
from handlers.common import main_menu

router = Router(name="premium_daily_vibe")

@router.message(F.text == "🗓 Daily Universal Vibe")
async def handle_daily_vibe(message: Message):
    result = get_daily_universal_vibe_forecast()
    await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
