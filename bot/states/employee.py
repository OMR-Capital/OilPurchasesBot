from aiogram.fsm.state import StatesGroup, State


class NewPurchaseState(StatesGroup):
    supplier = State()
    amount = State()
    contract_type = State()
    price = State()
    card = State()