from os import getenv

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models import User
router = Router()


@router.message(Command(commands=['create_root']))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()

    if message.chat.username != getenv('ROOT_USERNAME'):
        return

    user = User.register_user(
        'Mihail Butvin',
        'superuser'
    )
    await message.answer(user.access_key)
    


