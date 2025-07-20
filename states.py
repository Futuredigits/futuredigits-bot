from aiogram.fsm.state import StatesGroup, State

class LifePathStates(StatesGroup):
    waiting_for_birthdate = State()
