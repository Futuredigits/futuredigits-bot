from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states import CareerProfileStates
from db import get_user_language
from utils import (
    get_translation,
    handle_premium_lock,
    is_menu_command,
    route_menu_command,
    main_menu_keyboard,
    calculate_expression_number
)

@dp.message_handler(lambda message: message.text == get_translation(message.from_user.id, "career_profile_btn"), state="*")
async def handle_career_profile(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    description = {
        "en": "💼 *Career & Calling Insight*\nYou are not here by accident — your talents, drive, and inner rhythms point toward something unique.\nLet’s reveal the energy that guides your natural success path.\n\nPlease enter your *full name*:",
        "lt": "💼 *Karjeros ir Pašaukimo Įžvalga*\nJūs čia ne veltui — jūsų talentai, vidinė jėga ir natūralūs ritmai veda į išskirtinį kelią.\nAtskleiskime jūsų natūralios sėkmės energiją.\n\nĮveskite savo *pilną vardą*:",
        "ru": "💼 *Карьерный Профиль и Предназначение*\nВы здесь не случайно — ваши таланты, энергия и ритмы ведут к уникальному пути.\nДавайте откроем вашу природную энергию успеха.\n\nВведите *полное имя*:"
    }

    if await handle_premium_lock(message, user_id, lang, description.get(lang)):
        return

    await message.answer(description.get(lang), parse_mode="Markdown")
    await CareerProfileStates.waiting_for_name.set()

@dp.message_handler(state=CareerProfileStates.waiting_for_name)
async def process_career_profile(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    full_name = message.text.strip()

    if is_menu_command(full_name, user_id):
        await state.finish()
        await route_menu_command(message, state)
        return

    try:
        number = calculate_expression_number(full_name)
        lang = get_user_language(user_id)

        descriptions = {
            "en": {
                1: "Leadership, innovation, and independence are your core career traits. You're here to build and inspire.",
                2: "Harmony, diplomacy, and cooperation define your path. You're a master at building bridges.",
                3: "Your creative spirit thrives in self-expression, communication, and the arts. You light up any room.",
                4: "Discipline, systems, and steady growth. You're a builder of strong foundations.",
                5: "You’re meant to move — freedom, adaptability, and dynamic change fuel your purpose.",
                6: "You're a natural healer and nurturer. Service, care, and community light your success.",
                7: "You’re a deep thinker. Wisdom, teaching, and introspection define your true calling.",
                8: "You're made for power. Success, business, leadership, and financial mastery are your path.",
                9: "Your soul calls for purpose. You're here to serve, inspire, and lead through compassion.",
                11: "You're a visionary. Spiritual truth, intuition, and inspiration define your sacred work.",
                22: "You're a Master Builder. You’re here to manifest big dreams and leave legacy-level impact."
            },
            "lt": {
                1: "Liderystė, inovacijos ir nepriklausomybė. Esate čia tam, kad kurtumėte ir įkvėptumėte.",
                2: "Harmonija, diplomatija ir bendradarbiavimas – jūsų kelio esminiai bruožai.",
                3: "Kūrybiškumas, bendravimas ir menas. Jūs šviečiate scenoje ir gyvenime.",
                4: "Tvarka, struktūra ir stabilumas. Jūs statote tvirtus pamatus.",
                5: "Laisvė, pokyčiai ir judėjimas. Jus veda nuotykiai ir dinamika.",
                6: "Jūs esate natūralus globėjas – rūpinimasis, bendruomenė ir pasiaukojimas – jūsų sėkmė.",
                7: "Išmintis, analizė ir dvasinis gylis. Jūsų pašaukimas – mokyti ir suprasti.",
                8: "Galia, verslas ir finansinė sėkmė – tai jūsų kelias.",
                9: "Jūs čia tam, kad tarnautumėte žmonijai ir įkvėptumėte iš širdies.",
                11: "Vizija, intuicija ir įkvėpimas. Jūs – dvasinis švyturys.",
                22: "Didžių darbų kūrėjas. Jūsų misija – palikti ilgalaikį poveikį."
            },
            "ru": {
                1: "Лидерство, новаторство, независимость. Вы пришли, чтобы вдохновлять и создавать.",
                2: "Гармония, дипломатия, партнёрство — ваш путь строителя связей.",
                3: "Творчество, искусство, выражение. Вы сияете в любой среде.",
                4: "Структура, дисциплина, порядок. Вы создаёте прочные основы.",
                5: "Свобода, перемены, движение. Вы рождены меняться и вести.",
                6: "Забота, служение, сообщество. Ваша сила — в помощи другим.",
                7: "Мудрость, анализ, духовность. Ваш путь — в глубине знаний.",
                8: "Власть, бизнес, достижения. Вы рождены для успеха.",
                9: "Сострадание, гуманизм, служение. Ваша душа зовёт к великому.",
                11: "Вы — визионер. Интуиция, свет, вдохновение — ваш дар.",
                22: "Мастер-строитель. Ваша миссия — воплотить великое на Земле."
            }
        }

        header = {
            "en": "💼 *Your Career Energy*",
            "lt": "💼 *Jūsų Karjeros Energija*",
            "ru": "💼 *Ваша Энергия Карьеры*"
        }

        result = f"{header.get(lang)}\n{descriptions.get(lang, descriptions['en']).get(number)}"
        await message.answer(result, parse_mode="Markdown")
        await message.answer(get_translation(user_id, "done_choose_tool"), reply_markup=main_menu_keyboard(user_id))
        await state.finish()

    except:
        await message.answer(get_translation(user_id, "invalid_name"), parse_mode="Markdown")
