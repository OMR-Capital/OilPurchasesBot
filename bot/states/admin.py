from aiogram.fsm.state import StatesGroup, State


class AdminLoginState(StatesGroup):
    user_key = State()
    access_key = State()
    name = State()
