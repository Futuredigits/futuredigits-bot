# handlers/moon_energy.py
from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode

from localization import get_locale
from handlers.common import build_premium_menu
from tools.premium_moon_energy import get_moon_energy_result

router = Router(name="moon_energy")

# This tool needs no user input; it returns today's Moon Energy on trigger.
@router.message(lambda m: m.text and m.text.lower().strip() in {
    "moon", "🌙 moon energy", "moon energy", "/moon", "/moon_energy"
})
async def handle_moon_energy(message: Message):
    loc = get_locale(message.from_user.id)
    result = get_moon_energy_result(user_id=message.from_user.id, locale=loc)
    await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
