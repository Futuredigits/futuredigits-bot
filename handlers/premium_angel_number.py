from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.enums import ParseMode

from localization import _, get_locale
from tools.premium_angel_number import get_angel_number_result
from handlers.common import send_premium_menu  # if you don't have this, remove the last call

router = Router(name="premium_angel_number")

class AngelNumberStates(StatesGroup):
    waiting_for_sequence = State()

# ENTRY: user taps the Angel Number button -> we prompt and set state
@router.message(F.text.in_({_('btn_angel', 'en'), _('btn_angel', 'ru')}))
async def angel_start(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    intro = _("intro_angel_number", loc)
    await state.set_state(AngelNumberStates.waiting_for_sequence)
    await message.answer(intro, parse_mode=ParseMode.MARKDOWN)

# RESULT: user sends the sequence -> we decode and reply
@router.message(StateFilter(AngelNumberStates.waiting_for_sequence))
async def angel_result(message: Message, state: FSMContext):
    loc = get_locale(message.from_user.id)
    try:
        seq = (message.text or "").strip()
        text = get_angel_number_result(seq, user_id=message.from_user.id, locale=loc)
        await message.answer(text, parse_mode=ParseMode.MARKDOWN)
    except Exception:
        reprompt = _("angel_number_reprompt", loc) or _("intro_angel_number", loc)
        await message.answer(reprompt, parse_mode=ParseMode.MARKDOWN)
        return
    finally:
        await state.clear()

    # Optional: show premium menu again for smooth navigation (remove if you don't use it)
    try:
        await send_premium_menu(message.chat.id, loc)
    except Exception:
        pass
