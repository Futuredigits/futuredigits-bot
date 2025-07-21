from aiogram.fsm.state import StatesGroup, State

class LifePathStates(StatesGroup):
    waiting_for_birthdate = State()

class SoulUrgeStates(StatesGroup):
    waiting_for_full_name = State()

class PersonalityStates(StatesGroup):
    waiting_for_full_name = State()

