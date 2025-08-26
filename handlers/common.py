from aiogram import F, Router
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from localization import _, get_locale, set_locale, TRANSLATIONS
from aiogram.types import LabeledPrice, PreCheckoutQuery
import time
from datetime import datetime, timedelta, timezone
from db import redis

PRICES = {
    "monthly": 499,   # Stars
    "lifetime": 1999  # Stars
}


# --- Premium access flags
OWNER_ID = 619941697
PAID_USERS = set()
USED_TRIAL = set()

def is_premium_user(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in PAID_USERS

# --- FSM states 
from states import (
    LifePathStates,
    SoulUrgeStates,
    PersonalityStates,
    BirthdayStates,
    ExpressionStates,
    DestinyStates,
    PassionNumberStates,
    KarmicDebtStates,
    CompatibilityStates,
    LoveVibesStates,
    PersonalYearStates,
    AngelNumberStates,
    NameVibrationStates,
)

# --- Button keys 
MAIN_BTN_KEYS = [
    "btn_life_path",
    "btn_soul_urge",
    "btn_personality",
    "btn_birthday",
    "btn_expression",
    "btn_destiny",
]

PREMIUM_BTN_KEYS = [
    "btn_passion",
    "btn_karmic",
    "btn_compatibility",
    "btn_love",
    "btn_personal_year",
    "btn_moon",
    "btn_daily",
    "btn_angel",
    "btn_name_vibration",
]

# --- Helpers: labels & keyboards 
def label(locale: str, key: str) -> str:
    return TRANSLATIONS.get(locale, {}).get(key) or TRANSLATIONS["en"].get(key, key)

def build_main_menu(locale: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=label(locale, "btn_life_path")),
                KeyboardButton(text=label(locale, "btn_soul_urge")),
                KeyboardButton(text=label(locale, "btn_personality")),
            ],
            [
                KeyboardButton(text=label(locale, "btn_birthday")),
                KeyboardButton(text=label(locale, "btn_expression")),
                KeyboardButton(text=label(locale, "btn_destiny")),
            ],
            [KeyboardButton(text=label(locale, "btn_premium"))],
        ],
        resize_keyboard=True,
        input_field_placeholder=label(locale, "menu_main_placeholder"),
    )

def build_premium_menu(locale: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=label(locale, "btn_passion")),
                KeyboardButton(text=label(locale, "btn_karmic")),
                KeyboardButton(text=label(locale, "btn_compatibility")),
            ],
            [
                KeyboardButton(text=label(locale, "btn_love")),
                KeyboardButton(text=label(locale, "btn_personal_year")),
                KeyboardButton(text=label(locale, "btn_moon")),
            ],
            [
                KeyboardButton(text=label(locale, "btn_daily")),
                KeyboardButton(text=label(locale, "btn_angel")),
                KeyboardButton(text=label(locale, "btn_name_vibration")),
            ],
            [
                KeyboardButton(text=label(locale, "btn_upgrade")),
                KeyboardButton(text=label(locale, "btn_back")),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder=label(locale, "menu_premium_placeholder"),
    )

def build_lang_picker() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="English 🇬🇧", callback_data="lang_en"),
            InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru"),
        ]]
    )

# For routing: accept EN or RU captions
def all_captions_for(key: str) -> set[str]:
    return {
        TRANSLATIONS.get("en", {}).get(key, key),
        TRANSLATIONS.get("ru", {}).get(key, key),
    }

MAIN_CAPTIONS = set().union(*(all_captions_for(k) for k in MAIN_BTN_KEYS))
PREMIUM_CAPTIONS = set().union(*(all_captions_for(k) for k in PREMIUM_BTN_KEYS))

def caption_to_key(text: str) -> str | None:
    for k in MAIN_BTN_KEYS + PREMIUM_BTN_KEYS + ["btn_premium", "btn_back", "btn_upgrade"]:
        if text == TRANSLATIONS.get("en", {}).get(k) or text == TRANSLATIONS.get("ru", {}).get(k):
            return k
    return None

def _plan_label(loc: str, plan: str) -> str:
    if loc == "ru":
        return {"monthly": "1 месяц (подписка)", "lifetime": "Навсегда"}[plan]
    return {"monthly": "1 month (subscription)", "lifetime": "Lifetime"}[plan]

# --- Router
router = Router(name=__name__)

# --- /start: language picker
@router.message(CommandStart(), StateFilter("*"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="English 🇬🇧", callback_data="lang_en"),
            InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru"),
        ]]
    )
    await message.answer(_("choose_language"), reply_markup=kb, parse_mode=ParseMode.MARKDOWN)

@router.callback_query(F.data == "lang_en")
async def set_lang_en(callback: CallbackQuery):
    user_id = callback.from_user.id
    set_locale(user_id, "en")
    loc = "en"
    await callback.message.edit_text(_("lang_set_en", locale=loc))
    await callback.message.answer(
        _("start_message", locale=loc),
        reply_markup=build_main_menu(loc),
        parse_mode=ParseMode.MARKDOWN,
    )
    await callback.answer()

@router.callback_query(F.data == "lang_ru")
async def set_lang_ru(callback: CallbackQuery):
    user_id = callback.from_user.id
    set_locale(user_id, "ru")
    loc = "ru"
    await callback.message.edit_text(_("lang_set_ru", locale=loc))
    await callback.message.answer(
        _("start_message", locale=loc),
        reply_markup=build_main_menu(loc),
        parse_mode=ParseMode.MARKDOWN,
    )
    await callback.answer()


@router.callback_query(F.data.in_({"open_daily", "open_moon", "open_love"}))
async def notif_topic_open_cb(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    loc = get_locale(user_id)

    if not is_premium_user(user_id):
        if user_id in USED_TRIAL:
            await call.message.answer(
                _("premium_locked", locale=loc),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=build_premium_menu(loc),
            )
            await call.answer()
            return
        else:
            USED_TRIAL.add(user_id)
            await call.message.answer(_("premium_trial_granted", locale=loc), parse_mode=ParseMode.MARKDOWN)

    # Route by topic
    if call.data == "open_daily":
        from tools.premium_daily_vibe import get_daily_universal_vibe_forecast
        result = get_daily_universal_vibe_forecast(user_id=user_id, locale=loc)
        await call.message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))

    elif call.data == "open_moon":
        from tools.premium_moon_energy import get_moon_energy_forecast
        result = get_moon_energy_forecast(user_id=user_id, locale=loc)
        await call.message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))

    else:  # open_love
        await call.message.answer(_("intro_love_vibes", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.set_state(LoveVibesStates.waiting_for_full_name)

    await call.answer()

# --- /help
@router.message(Command("help"), StateFilter("*"))
async def help_handler(message: Message, state: FSMContext):
    await state.clear()
    loc = get_locale(message.from_user.id)
    await message.answer(_("help_text", locale=loc), parse_mode=ParseMode.MARKDOWN)

# --- /about
@router.message(Command("about"), StateFilter("*"))
async def about_handler(message: Message, state: FSMContext):
    await state.clear()
    loc = get_locale(message.from_user.id)
    await message.answer(
        _("about_text", locale=loc),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


# --- /language
@router.message(Command("language"), StateFilter("*"))
async def language_handler(message: Message, state: FSMContext):
    await state.clear()
    loc = get_locale(message.from_user.id)
    await message.answer(
        _("language_prompt", locale=loc),
        reply_markup=build_lang_picker(),
        parse_mode=ParseMode.MARKDOWN,
    )


# --- /premium CTA 
@router.message(Command("premium"), StateFilter("*"))
async def premium_handler(message: Message, state: FSMContext):
    await state.clear()
    loc = get_locale(message.from_user.id)
    await message.answer(
        _("premium_intro", locale=loc),
        reply_markup=_premium_kb(loc),
        disable_web_page_preview=True,
    )


def _premium_kb(loc: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("btn_buy_monthly", locale=loc),  callback_data="buy:monthly")],
        [InlineKeyboardButton(text=_("btn_buy_lifetime", locale=loc), callback_data="buy:lifetime")],
    ])

@router.message(F.text == TRANSLATIONS.get("en", {}).get("btn_upgrade", "💎 Upgrade Now"))
@router.message(F.text == TRANSLATIONS.get("ru", {}).get("btn_upgrade", "💎 Улучшить до Премиум"))
async def premium_cta_button(message: Message, state: FSMContext):
    await premium_handler(message, state)

# --- Premium menu 
@router.message(
    F.text.in_({
        TRANSLATIONS.get("en", {}).get("btn_premium", "🔓 Premium Tools"),
        TRANSLATIONS.get("ru", {}).get("btn_premium", "🔓 Премиум‑инструменты"),
    }),
    StateFilter("*")
)
async def show_premium_menu(message: Message, state: FSMContext):
    from notifications import add_subscriber
    await add_subscriber(message.from_user.id)
    await state.clear()
    loc = get_locale(message.from_user.id)
    await message.answer(
        _("premium_menu_intro", locale=loc),
        reply_markup=build_premium_menu(loc),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )

@router.message(
    F.text.in_({
        TRANSLATIONS.get("en", {}).get("btn_back", "🔙 Back to Main Menu"),
        TRANSLATIONS.get("ru", {}).get("btn_back", "🔙 Назад в главное меню"),
    }),
    StateFilter("*")
)
async def show_main_menu(message: Message, state: FSMContext):
    from notifications import add_subscriber
    await add_subscriber(message.from_user.id) 
    await state.clear()
    loc = get_locale(message.from_user.id)
    await message.answer(
        _("back_to_main_text", locale=loc),
        reply_markup=build_main_menu(loc),
        parse_mode=ParseMode.MARKDOWN,
    )

@router.callback_query(F.data.startswith("buy:"))
async def on_buy_plan(call: CallbackQuery):
    loc = get_locale(call.from_user.id)
    plan = call.data.split(":", 1)[1]
    if plan not in PRICES:
        await call.answer("Unknown plan", show_alert=True)
        return

    title = _("premium_invoice_title", locale=loc)
    desc  = _("premium_invoice_desc", locale=loc).format(plan=_plan_label(loc, plan))
    payload = f"premium:{plan}:{call.from_user.id}:{int(time.time())}"
    prices = [LabeledPrice(label=_plan_label(loc, plan), amount=PRICES[plan])]

    kwargs = {}
    if plan == "monthly":
        kwargs["subscription_period"] = 2592000  # 30 days (auto-renew)

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title=title,
        description=desc,
        payload=payload,
        currency="XTR",    # Telegram Stars
        prices=prices,
        **kwargs
    )
    await call.answer(_("toast_invoice_sent", locale=loc))

@router.pre_checkout_query()
async def on_pre_checkout(pre: PreCheckoutQuery):
    await pre.answer(ok=True)

async def _grant_premium(user_id: int, plan: str):
    now = datetime.now(timezone.utc)
    if plan == "lifetime":
        await redis.sadd("premium:lifetime", user_id)
        PAID_USERS.add(user_id)
    elif plan == "monthly":
        next_renewal = int((now + timedelta(days=30)).timestamp())
        await redis.hset("premium:sub_next_renewal", str(user_id), next_renewal)
        PAID_USERS.add(user_id)

@router.message(F.successful_payment)
async def on_successful_payment(message: Message):
    user_id = message.from_user.id
    loc = get_locale(user_id)

    payload = (message.successful_payment or {}).invoice_payload or ""
    plan = payload.split(":", 2)[1] if ":" in payload else "lifetime"

    await _grant_premium(user_id, plan)   
    await message.answer(
        _("premium_menu_intro", locale=loc),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=build_premium_menu(loc),
        disable_web_page_preview=True,
    )


# --- Unified Main Menu Handler 
@router.message(F.text.in_(MAIN_CAPTIONS), StateFilter("*"))
async def unified_main_menu_handler(message: Message, state: FSMContext):
    from notifications import add_subscriber
    await add_subscriber(message.from_user.id)
    choice_key = caption_to_key(message.text.strip())
    if not choice_key:
        return
    await state.clear()
    loc = get_locale(message.from_user.id)

    if choice_key == "btn_life_path":
        await message.answer(_("intro_life_path", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await state.set_state(LifePathStates.waiting_for_birthdate)

    elif choice_key == "btn_soul_urge":
        await message.answer(_("intro_soul_urge", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await state.set_state(SoulUrgeStates.waiting_for_full_name)

    elif choice_key == "btn_personality":
        await message.answer(_("intro_personality", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await state.set_state(PersonalityStates.waiting_for_full_name)

    elif choice_key == "btn_birthday":
        await message.answer(_("intro_birthday", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await state.set_state(BirthdayStates.waiting_for_birthdate)

    elif choice_key == "btn_expression":
        await message.answer(_("intro_expression", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await state.set_state(ExpressionStates.waiting_for_full_name)

    elif choice_key == "btn_destiny":
        await message.answer(_("intro_destiny", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_main_menu(loc))
        await state.set_state(DestinyStates.waiting_for_birthdate_and_name)

# --- Unified Premium Menu Handler
@router.message(F.text.in_(PREMIUM_CAPTIONS), StateFilter("*"))
async def unified_premium_menu_handler(message: Message, state: FSMContext):
    from notifications import add_subscriber
    await add_subscriber(message.from_user.id)
    user_id = message.from_user.id
    loc = get_locale(user_id)

    # Premium access check
    if is_premium_user(user_id):
        pass
    elif user_id in USED_TRIAL:
        await state.clear()
        await message.answer(
            _("premium_locked", locale=loc),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=build_premium_menu(loc)
        )
        return
    else:
        USED_TRIAL.add(user_id)
        await message.answer(_("premium_trial_granted", locale=loc), parse_mode=ParseMode.MARKDOWN)

    choice_key = caption_to_key(message.text.strip())
    if not choice_key:
        return

    await state.clear()

    if choice_key == "btn_passion":
        await message.answer(_("intro_passion", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.set_state(PassionNumberStates.waiting_for_full_name)

    elif choice_key == "btn_karmic":
        await message.answer(_("intro_karmic_debt", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.set_state(KarmicDebtStates.waiting_for_birthdate)

    elif choice_key == "btn_compatibility":
        await message.answer(_("intro_compatibility", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.set_state(CompatibilityStates.waiting_for_two_names)

    elif choice_key == "btn_love":
        await message.answer(_("intro_love_vibes", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.set_state(LoveVibesStates.waiting_for_full_name)

    elif choice_key == "btn_personal_year":
        await message.answer(_("intro_personal_year", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.set_state(PersonalYearStates.waiting_for_birthdate)

    elif choice_key == "btn_moon":
        from tools.premium_moon_energy import get_moon_energy_forecast
        result = get_moon_energy_forecast(user_id=user_id, locale=loc)  # <-- add args
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))


    elif choice_key == "btn_daily":
        from tools.premium_daily_vibe import get_daily_universal_vibe_forecast
        result = get_daily_universal_vibe_forecast(user_id=user_id, locale=loc)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))

    elif choice_key == "btn_angel":
        await message.answer(_("intro_angel_number", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.set_state(AngelNumberStates.waiting_for_number)

    elif choice_key == "btn_name_vibration":
        await message.answer(_("intro_name_vibration", locale=loc), parse_mode=ParseMode.MARKDOWN, reply_markup=build_premium_menu(loc))
        await state.set_state(NameVibrationStates.waiting_for_full_name)


@router.callback_query(F.data == "open_premium")
async def open_premium_cb(call: CallbackQuery):
    loc = get_locale(call.from_user.id)
    await call.message.answer(
        _("premium_intro", locale=loc),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=_premium_kb(loc),   
        disable_web_page_preview=True,
    )
    await call.answer()



# --- Exports 
def get_main_menu():
    return build_main_menu("en")

def register_common_handlers(dp):
    if router not in dp.sub_routers:
        dp.include_router(router)
