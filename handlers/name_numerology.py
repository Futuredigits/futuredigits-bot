from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import dp
from db import get_user_language
from utils import (
    get_translation,
    handle_premium_lock
)

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "name_numerology_btn"), state="*")
async def handle_name_numerology(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    # 🔐 Check premium access
    description = {
        "en": get_translation(user_id, "name_numerology"),
        "lt": get_translation(user_id, "name_numerology"),
        "ru": get_translation(user_id, "name_numerology")
    }

    if await handle_premium_lock(message, user_id, lang, description.get(lang)):
        return

    await message.answer(description.get(lang), parse_mode="Markdown")
