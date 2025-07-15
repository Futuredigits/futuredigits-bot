from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states import LuckyYearsStates
from db import get_user_language
from utils import (
    get_translation,
    handle_premium_lock,
    is_valid_date,
    main_menu_keyboard,
    is_menu_command,
    route_menu_command
)
import datetime

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "lucky_years_btn"), state="*")
async def handle_lucky_years(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    description = {
        "en": "📅 *Lucky Years Forecast*\nEvery soul moves in cycles. Some years are simply destined to align with your energy — years of clarity, breakthrough, love, expansion.\nLet’s discover the 3 most powerful years ahead that are perfectly in sync with your soul’s path.\n\nPlease enter your birthdate (DD.MM.YYYY):",
        "lt": "📅 *Sėkmingų Metų Prognozė*\nKiekviena siela juda ciklais. Kai kurie metai – tai šventi langai: proveržio, meilės, dvasinio pakilimo.\nAtraskime 3 artimiausius metus, kurie visiškai dera su jūsų sielos ritmu.\n\nĮveskite gimimo datą (DD.MM.YYYY):",
        "ru": "📅 *Прогноз Удачных Лет*\nДуша живёт в ритмах. Некоторые годы — это не случайность, а божественное совпадение с вашей судьбой.\nУзнаем 3 самых сильных года впереди, когда энергия будет в полном резонансе.\n\nВведите дату рождения (ДД.ММ.ГГГГ):"
    }

    if await handle_premium_lock(message, user_id, lang, description.get(lang)):
        return

    await message.answer(description.get(lang), parse_mode="Markdown")
    await LuckyYearsStates.waiting_for_birthdate.set()

@dp.message_handler(state=LuckyYearsStates.waiting_for_birthdate)
async def process_lucky_years(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    lang = get_user_language(user_id)

    if is_menu_command(text, user_id):
        await state.finish()
        await route_menu_command(message, state)
        return

    if not is_valid_date(text):
        await message.answer(get_translation(user_id, "invalid_format"), parse_mode="Markdown")
        return

    day, month, year = map(int, text.split('.'))
    now_year = datetime.datetime.now().year
    lucky_years = [now_year, now_year + 7, now_year + 14]

    result_msg = {
        "en": f"📅 *Your Lucky Years Are Calling*\nThese years are cosmic gateways for you — moments when the universe is quietly but powerfully on your side. Watch for signs, open your heart, and say yes to bold moves. These are your destined years:\n\n🔹 {lucky_years[0]}, {lucky_years[1]}, {lucky_years[2]}",
        "lt": f"📅 *Jūsų Sielos Derantys Metai*\nTai ne šiaip metai – tai kosminiai vartai jums. Šiuo metu visata tyliai padeda, atveria kelius, siunčia ženklus. Būkite atviri pokyčiams, drąsai ir meilei. Šie metai jums lemtingi:\n\n🔹 {lucky_years[0]}, {lucky_years[1]}, {lucky_years[2]}",
        "ru": f"📅 *Годы Космической Синхронизации*\nЭти годы — порталы судьбы для вашей души. Всё внутри и снаружи подталкивает вас к росту, любви и исполнению. В эти годы нужно быть смелым. Они — для вас:\n\n🔹 {lucky_years[0]}, {lucky_years[1]}, {lucky_years[2]}"
    }

    await message.answer(result_msg.get(lang), parse_mode="Markdown")
    await message.answer(get_translation(user_id, "done_choose_tool"), reply_markup=main_menu_keyboard(user_id))
    await state.finish()
