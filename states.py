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

class PassionNumberStates(StatesGroup):
    waiting_for_full_name = State()

class KarmicDebtStates(StatesGroup):
    waiting_for_birthdate = State()

class CompatibilityStates(StatesGroup):
    waiting_for_two_names = State()

class LoveVibesStates(StatesGroup):
    waiting_for_full_name = State()

class PersonalYearStates(StatesGroup):
    waiting_for_birthdate = State()

class AngelNumberStates(StatesGroup):
    waiting_for_number = State()

class NameVibrationStates(StatesGroup):
    waiting_for_full_name = State()







