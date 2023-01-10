from aiogram import Router
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from bot.callbacks.superuser import AccountsCallback, AccountsListCallback, UserInfoCallback
from bot import messages
from models import User

router = Router()


@router.callback_query(AccountsListCallback.filter())
async def accounts_list_handler(query: CallbackQuery):
    await query.answer()

    message = query.message
    if not message:
        return

    users = User.query(User.mode.not_contains('superuser')) # type: ignore
    users_list_kb = build_users_list_kb(users)
    await message.edit_text(
        text=messages.ACCOUNTS_LIST,
        reply_markup=users_list_kb
    )


def build_users_list_kb(users: list[User]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data=AccountsCallback().pack())]
    ])
    kb.inline_keyboard += [
        [
            InlineKeyboardButton(
                text=user.name, 
                callback_data=UserInfoCallback(key=user.key).pack()
            )
        ] for user in users
    ]

    return kb
