from aiogram.filters.callback_data import CallbackData


class MainPageCallback(CallbackData, prefix='employee.main_page'):
    pass


class NewPurchaseCallback(CallbackData, prefix='employee.new_purchase'):
    pass


class ContractTypeCallback(CallbackData, prefix='employee.new_purchase.contract_type'):
    cashless: bool


class HidePurchaseCallback(CallbackData, prefix='employee.hide_purchase'):
    pass
