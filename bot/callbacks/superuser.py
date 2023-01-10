from aiogram.filters.callback_data import CallbackData


class MainPageCallback(CallbackData, prefix='superuser.main_page'):
    pass


class AccountsCallback(CallbackData, prefix='superuser.accounts'):
    pass


class NewAdminCallback(CallbackData, prefix='superuser.accounts.new_admin'):
    pass


class NewEmployeeCallback(CallbackData, prefix='superuser.accounts.new_employee'):
    pass


class AccountsListCallback(CallbackData, prefix='superuser.accounts.accounts_list'):
    pass