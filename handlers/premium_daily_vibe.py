from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from tools.premium_daily_vibe import get_daily_universal_vibe_forecast
from handlers.common import build_premium_menu
from localization import TRANSLATIONS, get_locale

router = Router(name="premium_daily_vibe")

# Locale-agnostic trigger set
TRIGGERS = {
    "🗓 daily universal vibe",  # EN label lowercased
    "daily", "/daily", "/daily_vibe",
    "вибрация дня",            # common RU alias
}

# Add actual localized button labels from translations
for loc in ("en", "ru"):
    lbl = (TRANSLATIONS.get(loc, {}) or {}).get("btn_daily")
    if lbl:
        TRIGGERS.add(lbl.strip().lower())

@router.message(lambda m: m.text and m.text.strip().lower() in TRIGGERS)
async def handle_daily_vibe(message: Message):
    loc = get_locale(message.from_user.id)
    result = get_daily_universal_vibe_forecast(user_id=message.from_user.id, locale=loc)
    await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
