from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.superuser import (AccountsCallback, NewAdminCallback,
                                     NewEmployeeCallback)
from bot.handlers.common.error import error
from bot.handlers.utils import edit_message, get_init_message_id
from bot.states.superuser import NewUserState
from models import User

router = Router()


@router.callback_query(NewAdminCallback.filter())
async def new_admin_handler(query: CallbackQuery, state: FSMContext):
    await new_user_handler(query, state, 'admin')    


@router.callback_query(NewEmployeeCallback.filter())
async def new_employee_handler(query: CallbackQuery, state: FSMContext):
    await new_user_handler(query, state, 'employee')


async def new_user_handler(query: CallbackQuery, state: FSMContext, mode: str):
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
    await state.set_state(NewUserState.name)
    await state.update_data(init_message_id=message.message_id)
    await state.update_data(mode=mode)


@router.message(NewUserState.name, F.text)
async def name_handler(message: Message, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    name = message.text
    data = await state.get_data()
    mode = data.get('mode')
    if mode is None or name is None:
        return
        
    new_user = User.register_user(name, mode)
    if new_user is None:
        await error(message.chat.id, init_message_id, AccountsCallback().pack())
        return

    await edit_message(
        chat_id=message.chat.id,
        message_id=init_message_id,
        text=messages.SUCCESSFUL_CREATE_USER.format(
            name=new_user.name, 
            mode=new_user.mode, 
            access_key=new_user.access_key
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data=AccountsCallback().pack())]
        ])
    )
 
    await state.clear()
