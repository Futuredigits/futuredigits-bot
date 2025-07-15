from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import dp
from db import get_user_language
from utils import (
    get_translation,
    handle_premium_lock
)

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "detailed_compatibility_btn"), state="*")
async def handle_detailed_compatibility(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    # 🔐 Check premium access
    description = {
        "en": "🛠️ Detailed Compatibility will compare multiple numerology numbers between you and your partner. Coming soon...",
        "lt": "🛠️ Išsami Suderinamumo Analizė lygins kelis numerologinius skaičius tarp jūsų ir partnerio. Greitai pasirodys...",
        "ru": "🛠️ Подробная Совместимость сравнит несколько чисел между вами и партнёром. Скоро будет доступно..."
    }

    if await handle_premium_lock(message, user_id, lang, description.get(lang)):
        return

    await message.answer(description.get(lang), parse_mode="Markdown")
