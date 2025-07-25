from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Text

from tools.premium_moon_energy import get_moon_energy_forecast
from handlers.common import main_menu

router = Router(name="premium_moon_energy")

@router.message(Text("🌕 Moon Energy Today"))
async def handle_moon_energy(message: Message):
    result = get_moon_energy_forecast()
    await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu)
