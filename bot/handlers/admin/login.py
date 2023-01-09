from os import getenv

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot import messages
from bot.callbacks.admin import AdminLoginData
from bot.states.admin import AdminLoginState
from models import User

router = Router()


@router.callback_query(AdminLoginData.filter())
async def login_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    message = query.message
    if message is None:
        return
   
    await state.update_data(user_key=str(message.chat.id))
    await message.answer(messages.ASK_ACCESS_KEY)
    await state.set_state(AdminLoginState.access_key)


@router.message(AdminLoginState.access_key)
async def access_key_handler(message: Message, state: FSMContext):
    access_key = message.text
    if access_key == getenv('ADMIN_ACCESS_KEY', ''):
        await state.update_data(access_key=access_key)
        await message.answer(messages.ASK_NAME)
        await state.set_state(AdminLoginState.name)
    else:
        await message.answer(messages.WRONG_ACCESS_KEY)


@router.message(AdminLoginState.name, F.text)
async def name_handler(message: Message, state: FSMContext):
    name = message.text or ''
    await state.update_data(name=name)
    await login(message, state)


async def login(message: Message, state: FSMContext):
    data = await state.get_data()
    user_key, name = data['user_key'], data['name']

    admin = User(
        key=user_key,
        name=name,
        is_admin=True
    )
    admin.save()

    await state.clear()
    await message.answer(
        messages.SUCCESSFUL_ADMIN_LOGIN,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='История закупок', callback_data='test')]
        ])
    )