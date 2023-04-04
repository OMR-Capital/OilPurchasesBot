from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from bot import messages
from bot.callbacks.superuser import (AccountsListCallback, RemoveUserCallback,
                                     UserInfoCallback)
from models import User
from odetam.exceptions import ItemNotFound

router = Router()


@router.callback_query(UserInfoCallback.filter())
async def accounts_list_handler(query: CallbackQuery, callback_data: UserInfoCallback, state: FSMContext):
    await query.answer()
    await state.clear()
    
    message = query.message
    if not message:
        return

    try:
        user = User.get(callback_data.key) # type: ignore
    except ItemNotFound:
        return
    
    await message.edit_text(
        text=messages.USER_INFO.format(
            name=user.name,
            mode=user.mode,
            area=user.area,
            access_key=user.access_key
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
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