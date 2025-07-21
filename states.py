from aiogram.fsm.state import StatesGroup, State

class LifePathStates(StatesGroup):
    waiting_for_birthdate = State()

class SoulUrgeStates(StatesGroup):
    waiting_for_full_name = State()

class PersonalityStates(StatesGroup):
    waiting_for_full_name = State()

class BirthdayStates(StatesGroup):
    waiting_for_birthdate = State()

class ExpressionStates(StatesGroup):
    waiting_for_full_name = State()

class DestinyStates(StatesGroup):
    waiting_for_birthdate_and_name = State()

