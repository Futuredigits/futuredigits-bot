import os
import logging
from aiogram import Bot
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram import Router
main_router = Router()
from loader import bot, dp
from handlers import all_routers
for router in all_routers:
    dp.include_router(router)
from fastapi import FastAPI, Request
import uvicorn
import handlers
from db import set_user_language
from aiogram.fsm.context import FSMContext 
from utils import get_translation, main_menu_keyboard
from db import set_user_language, get_user_language, set_user_premium, is_user_premium


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@main_router.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()
    set_user_language(message.from_user.id, 'en')

    text = get_translation(message.from_user.id, "welcome")
    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu_keyboard(message.from_user.id))

    about_button = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="ℹ️ About", callback_data="about_info")]
        ]
    )
    await message.answer("ℹ️ Learn more about FutureDigits:", reply_markup=about_button)


   
@main_router.callback_query(lambda call: call.data == "about_info")
async def show_about_from_button(call: types.CallbackQuery):
    await call.message.answer(get_translation(call.from_user.id, "about"), parse_mode="Markdown")
    await call.answer()

@main_router.message(Command("help"))
async def send_help(message: types.Message, state: FSMContext):
    await state.clear() 

    help_text = (
        "📌 *FutureDigits Help Menu*\n\n"
        "Welcome! Here's what you can do:\n\n"
        "🔢 /start – Start the bot and choose your language\n"
        "🌟 Life Path, Soul Urge, Expression, Personality, Destiny, Birthday – Discover insights about yourself\n"
        "❤️ Compatibility – Compare two people by birthdates\n"
        "💎 Premium Tools – Explore advanced numerology tools (locked for now)\n"
        "🌍 /language – Change language (English, Lithuanian, Russian)\n\n"
        "If you need help at any time, just type /help ✨"
    )
    await message.answer(help_text, parse_mode="Markdown")


@main_router.message(Command("about"))
async def send_about(message: types.Message):
    text = get_translation(message.from_user.id, "about")
    await message.answer(text, parse_mode="Markdown")

@main_router.message(lambda message: message.text == get_translation(message.from_user.id, "back_to_menu"))
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🔙 You are back in the main menu. Choose a tool below 👇", reply_markup=main_menu_keyboard(message.from_user.id))

@main_router.message(Command("language"))
async def choose_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["English 🇬🇧", "Lietuvių 🇱🇹", "Русский 🇷🇺"]
    keyboard.add(*buttons)
    await message.answer("Choose your language / Pasirinkite kalbą / Выберите язык:", reply_markup=keyboard)

@main_router.message(lambda message: message.text in ["English 🇬🇧", "Lietuvių 🇱🇹", "Русский 🇷🇺"])
async def set_language(message: types.Message, state: FSMContext):
    await state.clear()  
    lang_map = {
        "English 🇬🇧": "en",
        "Lietuvių 🇱🇹": "lt",
        "Русский 🇷🇺": "ru"
    }
    selected_lang = lang_map[message.text]
    set_user_language(message.from_user.id, selected_lang)
    await message.answer(get_translation(message.from_user.id, "language_set"), reply_markup=main_menu_keyboard(message.from_user.id))


@main_router.message(Command("premium"))
async def send_premium_info(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    # Text block from translations.py
    text = get_translation(user_id, "premium_intro")

    # CTA button
    button_text = {
        "en": "🔓 Unlock Premium",
        "lt": "🔓 Atrakinti Premium",
        "ru": "🔓 Получить Premium"
    }

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        button_text.get(lang, button_text["en"]),
        callback_data="simulate_premium_payment"  # or "start_buy_premium"
    ))

    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)

@main_router.message(Command("set_premium"))
async def make_user_premium(message: types.Message):
    set_user_premium(message.from_user.id, True)
    await message.answer("✅ You are now a premium user.")

@main_router.message(Command("buy_premium"))
async def buy_premium(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    # Translated message
    text = {
        "en": (
            "💎 *FutureDigits Premium*\n\n"
            "Unlock all advanced numerology tools:\n"
            "• Lucky Years\n"
            "• Career Profile\n"
            "• Name Numerology\n"
            "• Love & Relationship Insights\n"
            "• Purpose & Mission Analysis\n\n"
            "💰 Price: *€9 one-time access*\n\n"
            "👉 This is a demo flow. Click below to simulate payment:"
        ),
        "lt": (
            "💎 *FutureDigits Premium*\n\n"
            "Atrakinkite visus pažangius numerologijos įrankius:\n"
            "• Sėkmingi Metai\n"
            "• Karjeros Profilis\n"
            "• Vardo Numerologija\n"
            "• Meilės ir Santykių Įžvalgos\n"
            "• Gyvenimo Paskirties Analizė\n\n"
            "💰 Kaina: *9 € vienkartinis mokestis*\n\n"
            "👉 Tai demonstracinė versija. Spauskite žemiau, kad imituotumėte mokėjimą:"
        ),
        "ru": (
            "💎 *FutureDigits Premium*\n\n"
            "Откройте все продвинутые нумерологические инструменты:\n"
            "• Удачные Годы\n"
            "• Карьерный Профиль\n"
            "• Нумерология Имени\n"
            "• Любовь и Отношения\n"
            "• Анализ Предназначения\n\n"
            "💰 Цена: *9 € однократный доступ*\n\n"
            "👉 Это демонстрация. Нажмите ниже, чтобы смоделировать оплату:"
        )
    }

    # Simulated "payment success" button
    button_text = {
        "en": "✅ Simulate Payment Success",
        "lt": "✅ Imituoti Sėkmingą Mokėjimą",
        "ru": "✅ Симулировать Успешную Оплату"
    }

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(button_text.get(lang, button_text["en"]), callback_data="simulate_premium_payment")
    )

    await message.answer(text.get(lang, text["en"]), reply_markup=keyboard, parse_mode="Markdown")

@main_router.message(lambda message: message.text == "💎 Premium Tools")
async def show_premium_menu(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "lucky_years_btn")),
        types.KeyboardButton(get_translation(user_id, "career_profile_btn"))
    )
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "name_numerology_btn")),
        types.KeyboardButton(get_translation(user_id, "lucky_colors_btn"))
    )
    keyboard.row(
        types.KeyboardButton(get_translation(user_id, "relationship_insights_btn")),
        types.KeyboardButton(get_translation(user_id, "purpose_analysis_btn"))
    )
    keyboard.add(types.KeyboardButton(get_translation(user_id, "detailed_compatibility_btn")))
    keyboard.add(types.KeyboardButton(get_translation(user_id, "back_to_menu")))

    descriptions = {
        "en": "💎 *Premium Tools*\nEnhance your life with advanced numerology insights. Choose a tool below 👇",
        "lt": "💎 *Premium Įrankiai*\nIšplėskite savo supratimą apie save naudodami pažangią numerologiją. Pasirinkite įrankį 👇",
        "ru": "💎 *Премиум Инструменты*\nУглубите понимание себя с помощью расширенной нумерологии. Выберите инструмент ниже 👇"
    }

    text = descriptions.get(lang, descriptions["en"])  # ✅ Fix: align this correctly

    if not is_user_premium(user_id):
        text += "\n\n🔒 " + get_translation(user_id, "premium_tool_locked")
        cta_button = types.InlineKeyboardMarkup()
        cta_button.add(types.InlineKeyboardButton(
            {
                "en": "🔓 Unlock Premium",
                "lt": "🔓 Atrakinti Premium",
                "ru": "🔓 Получить Premium"
            }.get(lang, "🔓 Unlock Premium"),
            callback_data="simulate_premium_payment"
        ))
        await message.answer(text, parse_mode="Markdown", reply_markup=cta_button)
    else:
        await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)


@main_router.callback_query(lambda call: call.data == "simulate_premium_payment")
async def handle_simulated_payment(call: types.CallbackQuery):
    user_id = call.from_user.id
    set_user_premium(user_id, True)

    confirmation = {
        "en": "🎉 *Payment successful!*\nYou now have full access to Premium tools.",
        "lt": "🎉 *Mokėjimas sėkmingas!*\nDabar turite prieigą prie visų Premium įrankių.",
        "ru": "🎉 *Оплата прошла успешно!*\nТеперь у вас есть доступ ко всем Premium инструментам."
    }

    await call.message.edit_reply_markup()  # remove button
    await call.message.answer(confirmation.get(get_user_language(user_id), confirmation["en"]), parse_mode="Markdown")


from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def on_startup(): 
    webhook_url = f"{os.getenv('WEBHOOK_BASE')}/webhook/{os.getenv('BOT_TOKEN')}"
    await bot.set_webhook(webhook_url)
    logging.info(f"✅ Webhook set to: {webhook_url}")


@app.post("/webhook/{token}")
async def telegram_webhook(token: str, request: Request):
    if token != os.getenv("BOT_TOKEN"):
        return {"error": "Invalid token"}
    update = await request.json()
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"status": "ok"}

@app.on_event("shutdown")
async def on_shutdown():
    session = await bot.get_session()  # ✅ safe and async
    await session.close()
    logging.info("✅ Bot session closed safely")

@app.get("/")
async def health_check():
    return {"status": "ok"}

dp.include_router(main_router)






