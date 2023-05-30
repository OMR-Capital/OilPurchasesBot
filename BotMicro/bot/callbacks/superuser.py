from aiogram.filters.callback_data import CallbackData

from models.user import UserMode


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
    user_mode: UserMode


class AcquirersCallback(CallbackData, prefix='superuser.acquirers'):
    pass


class NewAcquirerCallback(CallbackData, prefix='superuser.acquirers.new'):
    pass


class AcquirersListCallback(CallbackData, prefix='superuser.acquirers.list'):
    pass


class DeleteAcquirerCallback(CallbackData, prefix='superuser.acquirers.delete'):
    acquirer_key: str


class ConfirmDeleteAcquirerCallback(CallbackData, prefix='superuser.acquirers.confirm_delete'):
    acquirer_key: str


class EditPurchaseCallback(CallbackData, prefix='superuser.edit_purchase'):
    pass


class EditSkipCallback(CallbackData, prefix='superuser.edit_purchase.skip'):
    pass
