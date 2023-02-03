from os import getenv

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models import User
from statistic import update_fuelings_statistic, update_purchases_statistic

router = Router()


@router.message(Command(commands=['create_root']))
async def create_root_handler(message: Message, state: FSMContext):
    await state.clear()

    if message.chat.username != getenv('ROOT_USERNAME'):
        return

    user = User.register_user(
        'Mihail Butvin',
        'superuser'
    )
    await message.answer(user.access_key)
    

@router.message(Command(commands=['update_statistic']))
async def update_statistic_handler(message: Message, state: FSMContext):
    await state.clear()

    if message.chat.username != getenv('ROOT_USERNAME'):
        return
    
    update_purchases_statistic()
    update_fuelings_statistic()
    await message.answer('Statistic updated')
