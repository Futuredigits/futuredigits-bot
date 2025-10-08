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
import logging
import time
from datetime import datetime, timedelta, timezone
from db import redis

PRICES = {
    "monthly": 199,   # Stars
    "lifetime": 1999,  # Stars
    "daypass": 49
}


# --- Premium access flags
OWNER_ID = 619941697
PAID_USERS: set[int] = set()              
SUB_NEXT_RENEWAL: dict[int, int] = {}     
USED_TRIAL: set[int] = set()              

def is_premium_user(user_id: int) -> bool:
    """
    Restart-safe check:
    - OWNER always premium
    - Lifetime in PAID_USERS
    - Monthly if now < next_renewal in SUB_NEXT_RENEWAL
    """
    if user_id == OWNER_ID:
        return True
    if user_id in PAID_USERS:
        return True
    ts = SUB_NEXT_RENEWAL.get(user_id)
    return bool(ts and ts > int(time.time()))


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
    return TRANSLATIONS.get(locale, {}).get(key) or TRANSLATIONS.get("en", {}).get(key, key)


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

def is_main_caption(text: str | None) -> bool:
    if not text:
        return False
    k = caption_to_key(text.strip())
    return k in MAIN_BTN_KEYS

def is_premium_caption(text: str | None) -> bool:
    if not text:
        return False
    k = caption_to_key(text.strip())
    return k in PREMIUM_BTN_KEYS

def is_btn_premium(text: str | None) -> bool:
    return caption_to_key((text or "").strip()) == "btn_premium"

def is_btn_back(text: str | None) -> bool:
    return caption_to_key((text or "").strip()) == "btn_back"

def is_btn_upgrade(text: str | None) -> bool:
    return caption_to_key((text or "").strip()) == "btn_upgrade"



def _plan_label(loc: str, plan: str) -> str:
    if loc == "ru":
        return {
            "monthly": "1 месяц (подписка)",
            "lifetime": "Навсегда",
            "daypass": "1 день (день-пас)"
        }[plan]
    return {
        "monthly": "1 month (subscription)",
        "lifetime": "Lifetime",
        "daypass": "1 day (day pass)"
    }[plan]


# --- Router
router = Router(name=__name__)

# --- /start: language picker
@router.message(CommandStart(), StateFilter("*"))
async def start_handler(message: Message, state: FSMContext):
    from notifications import add_subscriber
    await add_subscriber(message.from_user.id)
    await state.clear()

    # --- Parse deep-link payload: "/start <payload>"
    parts = (message.text or "").split(maxsplit=1)
    payload = parts[1].strip() if len(parts) > 1 else ""
    user_id = message.from_user.id

    # Track first-touch acquisition source (ads) exactly once
    if payload.startswith("ad_"):
        exists = await redis.hexists("acq:campaign", str(user_id))
        if not exists:
            await redis.hset("acq:campaign", str(user_id), payload)

    # Track referral on first join only; prevent self-ref; idempotent
    if payload.startswith("ref_"):
        try:
            ref_id = int("".join(ch for ch in payload[4:] if ch.isdigit()))
        except Exception:
            ref_id = 0
        if ref_id and ref_id != user_id:
            # only set referrer once
            already = await redis.hexists("ref:referrer_of", str(user_id))
            if not already:
                await redis.hset("ref:referrer_of", str(user_id), ref_id)
                await redis.hincrby("ref:count", str(ref_id), 1)
                # Optional: store join timestamp for analytics
                await redis.hset("ref:joined_at", str(user_id), int(time.time()))

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[  # language picker
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

@router.message(Command("invite"), StateFilter("*"))
async def invite_handler(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    loc = get_locale(user_id)

    me = await message.bot.get_me()
    bot_username = me.username or "YourBot"

    # Personal link (deep link)
    link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    # Activated referral count
    act_raw = await redis.hget("ref:activated_count", str(user_id))
    activated = int(act_raw) if (act_raw and str(act_raw).isdigit()) else 0

    # Milestone logic: every 3 activations → +3 days premium
    milestone = (activated // 3) * 3
    last_awarded_raw = await redis.hget("ref:last_awarded", str(user_id))
    last_awarded = int(last_awarded_raw) if (last_awarded_raw and str(last_awarded_raw).isdigit()) else 0

    reward_note = ""
    if milestone > last_awarded:
        # Grant +3 days per full block achieved since last time
        blocks = (milestone - last_awarded) // 3
        days_to_add = 3 * blocks
        new_exp = await _extend_premium_days(user_id, days_to_add)
        await redis.hset("ref:last_awarded", str(user_id), milestone)

        # Localized reward line
        reward_note = _("invite_reward_granted", locale=loc) if TRANSLATIONS.get(loc, {}).get("invite_reward_granted") \
                      else "🎁 Premium extended for inviting friends!"
    
    title = TRANSLATIONS.get(loc, {}).get("invite_title",
        "✨ Invite friends — get Premium")
    body = TRANSLATIONS.get(loc, {}).get("invite_body",
        "Share your personal link. Every 3 activated friends → +3 days Premium.")
    stats = TRANSLATIONS.get(loc, {}).get("invite_stats",
        "Activated referrals: {count}. Invite {need} more to the next reward.").format(
            count=activated, need=(3 - (activated % 3) if activated % 3 != 0 else 3)
        )
    btn_text = TRANSLATIONS.get(loc, {}).get("invite_copy_button", "Copy link")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn_text, url=link)]
    ])

    text = f"{title}\n\n{body}\n\n🔗 {link}\n\n{stats}"
    if reward_note:
        text += f"\n\n{reward_note}"

    await message.answer(text, reply_markup=kb, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@router.message(Command("preload5000"))
async def preload_5000_stars(message: Message):
    # Owner-only guard
    if message.from_user.id != OWNER_ID:
        # stay silent for others
        return

    title = "Futuredigits • Stars Preload"
    description = (
        "Internal preload to move 5,000 Stars from your wallet "
        "to the bot’s earned balance (unlocks for Ads in ~21 days)."
    )

    # Amount is in whole Stars (XTR); no provider_token for Stars
    prices = [LabeledPrice(label="Preload 5,000 XTR", amount=5000)]

    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title=title,
        description=description,
        payload=f"preload:5000:{message.from_user.id}:{int(time.time())}",
        currency="XTR",
        prices=prices,
        disable_notification=True,
    )

    # Optional: quick UX hint
    await message.answer(
        "📦 Invoice created. If you already hold Stars in your wallet, "
        "Telegram will deduct them directly; otherwise it will offer to buy a Stars pack."
    )


# --- /premium CTA 
@router.message(Command("premium"), StateFilter("*"))
async def premium_handler(message: Message, state: FSMContext):
    from notifications import add_subscriber
    await add_subscriber(message.from_user.id)
    await state.clear()
    loc = get_locale(message.from_user.id)
    kb = await _premium_kb_with_link(message.bot, message.from_user.id, loc)
    await message.answer(
        _("premium_intro", locale=loc),
        parse_mode=ParseMode.HTML,
        reply_markup=kb,
        disable_web_page_preview=True,
    )   
    await message.answer(_("invoice_hint", locale=loc))




async def _premium_kb_with_link(bot, user_id: int, loc: str) -> InlineKeyboardMarkup:
    title   = _("premium_invoice_title", locale=loc)
    desc    = _("premium_invoice_desc",  locale=loc).format(plan=_plan_label(loc, "monthly"))
    payload = f"premium:monthly:{user_id}:{int(time.time())}"
    prices  = [LabeledPrice(label=_plan_label(loc, "monthly"), amount=PRICES["monthly"])]

    monthly_link = await bot.create_invoice_link(
        title=title,
        description=desc,
        payload=payload,
        currency="XTR",
        prices=prices,
        subscription_period=2592000  # exactly 30 days (required by Telegram)
    )

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("btn_buy_monthly",  locale=loc), url=monthly_link)],
        [InlineKeyboardButton(text=_("btn_buy_lifetime", locale=loc), callback_data="buy:lifetime")],
        [InlineKeyboardButton(text=_("btn_buy_daypass",  locale=loc), callback_data="buy:daypass")],
    ])


@router.message(F.text.func(is_btn_upgrade))
async def premium_cta_button(message: Message, state: FSMContext):
    await premium_handler(message, state)

# --- Premium menu 
@router.message(F.text.func(is_btn_premium), StateFilter("*"))
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


async def hydrate_premium_cache():
    try:
        # Reset mirrors
        PAID_USERS.clear()
        SUB_NEXT_RENEWAL.clear()

        # Lifetime users -> PAID_USERS
        lifetimes = await redis.smembers("premium:lifetime") or set()
        for u in lifetimes:
            s = u.decode() if isinstance(u, (bytes, bytearray)) else str(u)
            if s.isdigit():
                PAID_USERS.add(int(s))

        # Monthly: load next-renewal timestamps, and warm active users into PAID_USERS
        h = await redis.hgetall("premium:sub_next_renewal") or {}
        now_ts = int(time.time())
        for k, v in h.items():
            ks = k.decode() if isinstance(k, (bytes, bytearray)) else str(k)
            vs = v.decode() if isinstance(v, (bytes, bytearray)) else str(v)
            try:
                uid = int(ks)
                ts = int(vs)
                SUB_NEXT_RENEWAL[uid] = ts
                if ts > now_ts:
                    PAID_USERS.add(uid)  # warm active monthly subs as paid
            except Exception:
                continue

        logging.info(f"[premium] hydrated: lifetime={len(PAID_USERS)} monthly={len(SUB_NEXT_RENEWAL)}")
    except Exception as e:
        logging.exception(f"[premium] hydrate failed: {e}")



@router.message(F.text.func(is_btn_back), StateFilter("*"))
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
    user_id = call.from_user.id
    loc = get_locale(user_id)
    plan = call.data.split(":", 1)[1]

    if plan not in PRICES:
        await call.answer("Unknown plan", show_alert=True)
        return

    title   = _("premium_invoice_title", locale=loc)
    desc    = _("premium_invoice_desc",  locale=loc).format(plan=_plan_label(loc, plan))
    payload = f"premium:{plan}:{user_id}:{int(time.time())}"
    prices  = [LabeledPrice(label=_plan_label(loc, plan), amount=PRICES[plan])]

    if plan == "monthly":
        # Subscriptions must use createInvoiceLink with subscription_period
        link = await call.bot.create_invoice_link(
            title=title,
            description=desc,
            payload=payload,
            currency="XTR",
            prices=prices,
            subscription_period=2592000  # exactly 30 days, the only allowed value
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=_("btn_buy_monthly", locale=loc), url=link)],
            [InlineKeyboardButton(text=_("btn_buy_lifetime", locale=loc), callback_data="buy:lifetime")],
            [InlineKeyboardButton(text=_("btn_buy_daypass",  locale=loc), callback_data="buy:daypass")],
        ])
        await call.message.answer(_("premium_intro", locale=loc), reply_markup=kb, disable_web_page_preview=True)
        await call.answer()
        return

    # Lifetime (one-time) stays as an in-chat Stars invoice
    await call.bot.send_invoice(
        chat_id=user_id,
        title=title,
        description=desc,
        payload=payload,
        currency="XTR",
        prices=prices,
    )
    await call.answer(_("toast_invoice_sent", locale=loc))

@router.pre_checkout_query()
async def on_pre_checkout(pre: PreCheckoutQuery):
    await pre.answer(ok=True)

async def _grant_premium(user_id: int, plan: str, *, expires_ts: int | None = None, charge_id: str | None = None):
    
    now = datetime.now(timezone.utc)
    if plan == "lifetime":
        await redis.sadd("premium:lifetime", user_id)
        PAID_USERS.add(user_id)
    elif plan == "monthly":
        if not expires_ts:
            expires_ts = int((now + timedelta(days=30)).timestamp())
        await redis.hset("premium:sub_next_renewal", str(user_id), int(expires_ts))
        if charge_id:
            await redis.hset("premium:last_charge_id", str(user_id), charge_id)
        PAID_USERS.add(user_id)
    elif plan == "daypass":          
        await _extend_premium_days(user_id, 1)


@router.message(F.successful_payment)
async def on_successful_payment(message: Message):
    user_id = message.from_user.id
    loc = get_locale(user_id)

    sp = message.successful_payment
    payload = (sp or {}).invoice_payload or ""
    plan = payload.split(":", 2)[1] if ":" in payload else "lifetime"

    try:
        
        expires_ts = getattr(sp, "subscription_expiration_date", None)
        if isinstance(expires_ts, datetime):
            
            expires_ts = int(expires_ts.replace(tzinfo=timezone.utc).timestamp())
        elif isinstance(expires_ts, (int, float)):
            expires_ts = int(expires_ts)
        else:
            expires_ts = None

        charge_id = getattr(sp, "telegram_payment_charge_id", None)
    except Exception:
        expires_ts = None
        charge_id = None

    await _grant_premium(user_id, plan, expires_ts=expires_ts, charge_id=charge_id)

    await message.answer(
        _("payment_success", locale=loc),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=build_premium_menu(loc),
        disable_web_page_preview=True,
    )


# --- Unified Main Menu Handler 
@router.message(F.text.func(is_main_caption), StateFilter("*"))
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
@router.message(F.text.func(is_premium_caption), StateFilter("*"))
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
async def open_premium_cb(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    loc = get_locale(user_id)
    await state.clear()

    if is_premium_user(user_id):
        await call.message.answer(
            _("premium_menu_intro", locale=loc),
            reply_markup=build_premium_menu(loc),
            disable_web_page_preview=True,
        )
    else:
        kb = await _premium_kb_with_link(call.bot, user_id, loc)
        await call.message.answer(
            _("premium_intro", locale=loc),
            parse_mode=ParseMode.HTML,
            reply_markup=kb,
            disable_web_page_preview=True,
        )
    await call.answer()


async def mark_activation_once(user_id: int) -> None:   
    already = await redis.sismember("ref:activated_users", str(user_id))
    if already:
        return    
    await redis.sadd("ref:activated_users", str(user_id))
   
    ref_raw = await redis.hget("ref:referrer_of", str(user_id))
    if not ref_raw:
        return
    
    try:
        ref_id = int(ref_raw if isinstance(ref_raw, (str, int)) else ref_raw.decode())
    except Exception:
        return
    if ref_id <= 0 or ref_id == user_id:
        return
    
    await redis.hincrby("ref:activated_count", str(ref_id), 1)    
    await redis.hset("ref:activated_at", str(user_id), int(time.time()))


async def _grant_trial_days(user_id: int, days: int = 3):
    from datetime import datetime, timedelta, timezone
    now = int(datetime.now(timezone.utc).timestamp())
    exp = now + days * 24 * 60 * 60

    # Reuse existing storage to mark as premium until exp:
    await redis.hset("premium:sub_next_renewal", str(user_id), exp)

    # Warm in-memory mirrors immediately (no restart needed)
    SUB_NEXT_RENEWAL[user_id] = exp
    PAID_USERS.add(user_id)


async def _extend_premium_days(user_id: int, days: int) -> int:
    
    now = int(datetime.now(timezone.utc).timestamp())
    
    cur_raw = await redis.hget("premium:sub_next_renewal", str(user_id))
    cur = int(cur_raw) if (cur_raw and str(cur_raw).isdigit()) else 0

    base = max(now, cur)
    new_exp = base + days * 24 * 60 * 60

    await redis.hset("premium:sub_next_renewal", str(user_id), new_exp)
    
    SUB_NEXT_RENEWAL[user_id] = new_exp
    PAID_USERS.add(user_id)

    return new_exp



# --- Exports 
def get_main_menu():
    return build_main_menu("en")

def register_common_handlers(dp):
    if router not in dp.sub_routers:
        dp.include_router(router)
