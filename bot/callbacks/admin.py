from aiogram.filters.callback_data import CallbackData


class MainPageCallback(CallbackData, prefix='admin.main_page'):
    pass


class ApprovePurchaseCallback(CallbackData, prefix='admin.approve_purchase'):
    purchase: str


class StatisticCallback(CallbackData, prefix='admin.statistic'):
    pass