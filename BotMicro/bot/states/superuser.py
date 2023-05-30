from aiogram.fsm.state import StatesGroup, State


class NewUserState(StatesGroup):
    name = State()
    area = State()


class NewAcquirerState(StatesGroup):
    name = State()


class EditPurchaseState(StatesGroup):
    key = State()
    contract_type = State()
    client_type = State()
    supplier = State()
    unit = State()
    amount = State()
    inn = State()
    price = State()
    card = State()
    bank = State()
