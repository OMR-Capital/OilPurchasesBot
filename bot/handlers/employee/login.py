from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import messages
from bot.callbacks.employee import EmployeeLoginData
from bot.states.employee import EmployeeLoginState
from models import User

router = Router()


@router.callback_query(EmployeeLoginData.filter())
async def login_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    message = query.message
    if message is None:
        return
    
    await state.update_data(user_key=str(message.chat.id))
    await message.answer(messages.ASK_NAME)
    await state.set_state(EmployeeLoginState.name)


@router.message(EmployeeLoginState.name, F.text)
async def name_handler(message: Message, state: FSMContext):
    name = message.text or ''
    await state.update_data(name=name)
    await login(message, state)


async def login(message: Message, state: FSMContext):
    data = await state.get_data()
    user_key, name = data['user_key'], data['name']

    employee = User(
        key=user_key,
        name=name,
        is_admin=False
    )
    employee.save()

    await state.clear()
    await message.answer(messages.SUCCESSFUL_EMPLOYEE_LOGIN)
