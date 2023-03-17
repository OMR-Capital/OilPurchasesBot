from aiogram.fsm.state import StatesGroup, State


class NewUserState(StatesGroup):
    name = State()

