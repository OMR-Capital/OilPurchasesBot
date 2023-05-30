from typing import Literal

from aiogram.filters.callback_data import CallbackData

from models.purchase import ClientType, ContractType, Unit


class MainPageCallback(CallbackData, prefix='employee.main_page'):
    pass


class NewPurchaseCallback(CallbackData, prefix='employee.new_purchase'):
    pass


class UnitCallback(CallbackData, prefix='employee.new_purchase.unit'):
    unit: Unit


class ContractTypeCallback(CallbackData, prefix='employee.new_purchase.contract_type'):
    contract_type: ContractType


class ClientTypeCallback(CallbackData, prefix='employee.new_purchase.contract_type'):
    client_type: ClientType


class HidePurchaseCallback(CallbackData, prefix='employee.hide_purchase'):
    pass


class NewFuelingCallback(CallbackData, prefix='employee.new_fueling'):
    pass


class FuelingCostCallback(CallbackData, prefix='employee.new_fueling.cost'):
    cost: int


class NewDispatchCallback(CallbackData, prefix='new_dis'):
    pass


class AcquirerCallback(CallbackData, prefix='dis.acquirer'):
    acquirer_key: str


class ConfirmDispatchCallback(CallbackData, prefix='dis.conf'):
    pass


class HideDispatchCallback(CallbackData, prefix='hide_dis'):
    pass