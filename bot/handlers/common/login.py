from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import messages
from bot.handlers import admin, superuser, employee
from bot.callbacks.common import LoginCallback
from bot.states.common import LoginState
from models import User

router = Router()


@router.callback_query(LoginCallback.filter())
async def login_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()  

    message = query.message
    if not message:
        return

    await message.answer(messages.ASK_ACCESS_KEY)
    await state.set_state(LoginState.access_key)


@router.message(LoginState.access_key, F.text)
async def access_key_handler(message: Message, state: FSMContext):
    access_key = message.text 
    result = User.query(User.access_key == access_key)

    if len(result) == 0:
        await message.answer(messages.WRONG_ACCESS_KEY)
        return 
        
    user = result.pop()
    user.chat_id = message.chat.id
    user.save()

    if user.mode == 'superuser':
        await superuser.greet(message, user)
    elif user.mode == 'admin':
        await admin.greet(message, user)
    elif user.mode == 'employee':
        await employee.greet(message, user)

    await state.clear()
    
    