from typing import Literal
from aiogram.filters.callback_data import CallbackData


class MainPageCallback(CallbackData, prefix='employee.main_page'):
    pass


class NewPurchaseCallback(CallbackData, prefix='employee.new_purchase'):
    pass


class UnitCallback(CallbackData, prefix='employee.new_purchase.unit'):
    unit: Literal['liter', 'kg']


class ContractTypeCallback(CallbackData, prefix='employee.new_purchase.contract_type'):
    cashless: bool


class ClientTypeCallback(CallbackData, prefix='employee.new_purchase.contract_type'):
    from_manager: bool


class HidePurchaseCallback(CallbackData, prefix='employee.hide_purchase'):
    pass


class NewFuelingCallback(CallbackData, prefix='employee.new_fueling'):
    pass


class FuelingCostCallback(CallbackData, prefix='employee.new_fueling.cost'):
    cost: int


class NewDispatchCallback(CallbackData, prefix='new_dis'):
    pass


class DestinationCallback(CallbackData, prefix='dis.dest'):
    destination: str
    

class ConfirmDispatchCallback(CallbackData, prefix='dis.conf'):
    pass


class HideDispatchCallback(CallbackData, prefix='hide_dis'):
    pass