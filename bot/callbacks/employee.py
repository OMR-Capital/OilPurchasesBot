from aiogram.filters.callback_data import CallbackData


class MainPageCallback(CallbackData, prefix='employee.main_page'):
    pass


class NewPurchaseCallback(CallbackData, prefix='employee.new_purchase'):
    pass


class HidePurchaseCallback(CallbackData, prefix='employee.hide_purchase'):
    pass
