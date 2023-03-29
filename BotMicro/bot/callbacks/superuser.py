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


class UserInfoCallback(CallbackData, prefix='superuser.accounts.user_info'):
    key: str


class RemoveUserCallback(CallbackData, prefix='superuser.accounts.remove_user'):
    key: str


class AmountStatisticsCallback(CallbackData, prefix='superuser.amount_statistics'):
    pass