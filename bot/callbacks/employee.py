from aiogram.filters.callback_data import CallbackData


class MainPageCallback(CallbackData, prefix='employee.main_page'):
    pass


class NewPurchaseCallback(CallbackData, prefix='employee.new_purchase'):
    pass


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
    