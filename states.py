from aiogram.fsm.state import StatesGroup, State

class LifePathStates(StatesGroup):
    waiting_for_birthdate = State()

class CompatibilityStates(StatesGroup):
    waiting_for_first_date = State()
    waiting_for_second_date = State()

class SoulUrgeStates(StatesGroup):
    waiting_for_name = State()

class ExpressionStates(StatesGroup):
    waiting_for_name = State()

class PersonalityStates(StatesGroup):
    waiting_for_name = State()

class DestinyStates(StatesGroup):
    waiting_for_name = State()

class BirthdayStates(StatesGroup):
    waiting_for_birthdate = State()

class LuckyYearsStates(StatesGroup):
    waiting_for_birthdate = State()

class CareerProfileStates(StatesGroup):
    waiting_for_name = State()







