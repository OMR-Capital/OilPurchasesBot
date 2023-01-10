from aiogram.filters.callback_data import CallbackData


class LoginCallback(CallbackData, prefix='common.login'):
    pass