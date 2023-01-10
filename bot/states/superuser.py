from aiogram.fsm.state import StatesGroup, State


class NewAdminState(StatesGroup):
    name = State()


class NewEmployeeState(StatesGroup):
    name = State()