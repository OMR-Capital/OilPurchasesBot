from random import choices
from string import ascii_lowercase, digits

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.superuser import AccountsCallback, NewEmployeeCallback
from bot.handlers.utils import edit_message, get_init_message_id
from bot.states.superuser import NewEmployeeState
from models import User

router = Router()


@router.callback_query(NewEmployeeCallback.filter())
async def new_employee_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.ASK_NAME,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Отмена', callback_data=AccountsCallback().pack())]
        ])
    )
    await state.set_state(NewEmployeeState.name)
    await state.update_data(init_message_id=message.message_id)


@router.message(NewEmployeeState.name, F.text)
async def name_handler(message: Message, state: FSMContext):
    await message.delete()

    name = message.text or ''
    access_key = ''.join(choices(ascii_lowercase + digits, k=6))

    new_employee = User(
        access_key=access_key,
        mode='employee',
        name=name
    )
    new_employee.save()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await edit_message(
        chat_id=message.chat.id,
        message_id=init_message_id,
        text=messages.SUCCESSFUL_CREATE_USER.format(
            name=new_employee.name, 
            mode=new_employee.mode, 
            access_key=new_employee.access_key
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data=AccountsCallback().pack())]
        ])
    )
 
    await state.clear()
