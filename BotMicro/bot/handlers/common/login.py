from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import messages
from bot.callbacks.common import LoginCallback
from bot.handlers import admin, employee, superuser
from bot.handlers.utils import edit_message, get_init_message_id
from bot.states.common import LoginState
from models import User
from models.user import UserMode

router = Router()


@router.callback_query(LoginCallback.filter())
async def login_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await message.edit_text(messages.ASK_ACCESS_KEY, reply_markup=None)
    await state.update_data(init_message_id=message.message_id)
    await state.set_state(LoginState.access_key)


@router.message(LoginState.access_key, F.text)
async def access_key_handler(message: Message, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    access_key = message.text or ''
    user = User.login_user(access_key, message.chat.id)

    if not user:
        await edit_message(message.chat.id, init_message_id, messages.WRONG_ACCESS_KEY)
        return

    if user.mode == UserMode.SUPERUSER:
        await superuser.greet(message.chat.id, init_message_id, user)
    elif user.mode == UserMode.ADMIN:
        await admin.greet(message.chat.id, init_message_id, user)
    elif user.mode == UserMode.EMPLOYEE:
        await employee.greet(message.chat.id, init_message_id, user)

    await state.clear()
