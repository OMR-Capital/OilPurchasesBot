from aiogram.fsm.state import StatesGroup, State


class EmployeeLoginState(StatesGroup):
    user_key = State()
    name = State()
