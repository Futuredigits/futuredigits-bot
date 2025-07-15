from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from db import get_user_language
from utils import (
    get_translation,
    handle_premium_lock
)

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "lucky_colors_btn"), state="*")
async def handle_lucky_colors(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    # 🔐 Check premium access
    description = {
        "en": get_translation(user_id, "lucky_colors"),
        "lt": get_translation(user_id, "lucky_colors"),
        "ru": get_translation(user_id, "lucky_colors")
    }

    if await handle_premium_lock(message, user_id, lang, description.get(lang)):
        return

    await message.answer(description.get(lang), parse_mode="Markdown")
