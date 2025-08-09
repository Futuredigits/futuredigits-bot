from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from tools.premium_moon_energy import get_moon_energy_forecast
from handlers.common import build_premium_menu
from localization import _, get_locale

router = Router(name="premium_moon_energy")

@router.message(F.text == "🌕 Moon Energy Today")
async def handle_moon_energy(message: Message):
    result = get_moon_energy_forecast()
    await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=premium_menu)
