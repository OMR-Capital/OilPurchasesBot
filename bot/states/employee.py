from aiogram.fsm.state import StatesGroup, State


class NewPurchaseState(StatesGroup):
    supplier = State()
    amount = State()
    client_type = State()
    contract_type = State()
    inn = State()
    price = State()
    card = State()
    bank = State()


class NewFueling(StatesGroup):
    cost = State()
    