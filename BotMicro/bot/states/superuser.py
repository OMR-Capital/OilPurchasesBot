from aiogram.fsm.state import StatesGroup, State


class NewUserState(StatesGroup):
    name = State()
    area = State()


class NewAcquirerState(StatesGroup):
    name = State()
    