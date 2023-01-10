from aiogram.filters.callback_data import CallbackData


class MainPageCallback(CallbackData, prefix='superuser.main_page'):
    pass


class AccountsCallback(CallbackData, prefix='superuser.accounts'):
    pass