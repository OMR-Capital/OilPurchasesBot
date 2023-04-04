from aiogram.fsm.state import StatesGroup, State


class NewPurchaseState(StatesGroup):
    contract_type = State()
    client_type = State()
    supplier = State()
    unit = State()
    amount = State()
    inn = State()
    price = State()
    card = State()
    bank = State()


class NewDispatchState(StatesGroup):
    destination = State()
    unit = State()
    amount = State()
    confirm = State()


class NewFueling(StatesGroup):
    cost = State()
     