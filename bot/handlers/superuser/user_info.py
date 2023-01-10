from aiogram import Router
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from bot.callbacks.superuser import AccountsListCallback, UserInfoCallback, RemoveUserCallback
from bot import messages
from models import User

router = Router()


@router.callback_query(UserInfoCallback.filter())
async def accounts_list_handler(query: CallbackQuery, callback_data: UserInfoCallback):
    await query.answer()

    message = query.message
    if not message:
        return

    user = User.get(callback_data.key) # type: ignore
    if not user:
        return

    await message.edit_text(
        text=messages.USER_INFO.format(
            name=user.name,
            mode=user.mode,
            access_key=user.access_key
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='История закупок', callback_data='test')],
            [
                InlineKeyboardButton(
                    text='❌ Удалить ❌', 
                    callback_data=RemoveUserCallback(key=callback_data.key).pack()
                )
            ],
            [InlineKeyboardButton(text='Назад', callback_data=AccountsListCallback().pack())],
        ])
    )


@router.callback_query(RemoveUserCallback.filter())
async def remove_user_handler(query: CallbackQuery, callback_data: RemoveUserCallback):
    await query.answer()
    message = query.message
    if not message:
        return

    User.delete_key(callback_data.key) # type: ignore

    await message.edit_text(
        text=messages.SUCCESSFUL_DELETE_USER,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data=AccountsListCallback().pack())]
        ])
    )