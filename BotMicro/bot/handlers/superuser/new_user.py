from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.superuser import (AccountsCallback, NewAdminCallback,
                                     NewEmployeeCallback)
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
    await state.update_data(init_message_id=message.message_id, mode=mode)


@router.message(NewUserState.name, F.text)
async def name_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    await state.update_data(name=message.text)

    data = await state.get_data()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=messages.ASK_AREA,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Отмена', callback_data=AccountsCallback().pack())]
        ])
    )
    await state.set_state(NewUserState.area)


@router.message(NewUserState.area, F.text)
async def area_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    if message.text is None:
        return

    data = await state.get_data()
    new_user = User.register_user(name=data['name'], area=message.text, mode=data['mode'])
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=messages.SUCCESSFUL_CREATE_USER.format(
            name=new_user.name,
            mode=new_user.mode,
            area=new_user.area,
            access_key=new_user.access_key
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data=AccountsCallback().pack())]
        ])
    )

    await state.clear()
