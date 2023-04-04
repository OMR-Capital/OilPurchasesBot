from aiogram.fsm.state import StatesGroup, State


class LoginState(StatesGroup):
    access_key = State()