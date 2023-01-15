from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import messages
from bot.callbacks.common import LoginCallback
from models import User

router = Router()


@router.message(Command(commands=['logout']))
async def logout_handler(message: Message, state: FSMContext):
    await state.clear()

    users = User.query(User.chat_id == message.chat.id)
    for user in users:
        user.chat_id = None

    User.put_many(users)

    await message.answer(
        messages.START,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Войти', callback_data=LoginCallback().pack())]
        ])
    )
    await message.delete()
