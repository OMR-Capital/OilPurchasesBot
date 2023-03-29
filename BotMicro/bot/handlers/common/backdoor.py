from asyncio import gather
from os import getenv
from time import time

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models import User
from models.purchase import Purchase
from utils.statistic.purchases import add_purchase_stats, get_statistic_data

router = Router()


@router.message(Command(commands=['create_root']))
async def create_root_handler(message: Message, state: FSMContext):
    await state.clear()

    if message.chat.username != getenv('ROOT_USERNAME'):
        return

    user = User.register_user(
        'Mihail Butvin',
        'N',
        'superuser'
    )
    await message.answer(user.access_key)


@router.message(Command(commands=['update_statistic']))
async def update_statistic_handler(message: Message, state: FSMContext):
    if message.chat.username != getenv('ROOT_USERNAME'):
        return await message.answer('You are not superuser')
         
    await state.clear()
    await message.answer('Wait...')

    try:
        purchases = Purchase.get_all()
        await add_purchase_stats(purchases[0])
        # await message.answer(str(result))
        # await message.answer(f'Updated {len(result)} purchases in {time() - st} seconds')
    except Exception as e:
        await message.answer(str(e))
