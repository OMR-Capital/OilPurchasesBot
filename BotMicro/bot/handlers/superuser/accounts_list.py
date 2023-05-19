from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.superuser import (AccountsCallback, AccountsListCallback,
                                     UserInfoCallback)
from models import User
from models.user import UserMode

router = Router()


@router.callback_query(AccountsListCallback.filter())
async def accounts_list_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await state.clear()

    users = User.query(User.mode != UserMode.SUPERUSER)  # type: ignore
    users_list_kb = build_users_list_kb(users)
    await message.edit_text(
        text=messages.ACCOUNTS_LIST,
        reply_markup=users_list_kb
    )


def build_users_list_kb(users: list[User]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'{user.name} - {UserMode.get_name(user.mode)}',
                callback_data=UserInfoCallback(key=user.key).pack()  # type: ignore
            )
        ] for user in users
    ])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data=AccountsCallback().pack())
    ])

    return kb
