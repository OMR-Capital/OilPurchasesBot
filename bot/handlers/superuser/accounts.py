from aiogram import Router
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.superuser import (AccountsCallback, AccountsListCallback,
                                     MainPageCallback, NewAdminCallback,
                                     NewEmployeeCallback)

router = Router()


@router.callback_query(AccountsCallback.filter())
async def accounts_handler(query: CallbackQuery):
    await query.answer()

    message = query.message
    if not message:
        return

    await open_accounts(message)


async def open_accounts(message: Message):
    await message.edit_text(
        messages.ACCOUNTS,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Новый Админ', callback_data=NewAdminCallback().pack()), 
                InlineKeyboardButton(text='Новый Работник', callback_data=NewEmployeeCallback().pack())
            ],
            [
                InlineKeyboardButton(text='Список аккаунтов', callback_data=AccountsListCallback().pack()), 
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack()), 
            ],
        ])
    )