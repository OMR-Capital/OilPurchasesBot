from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.superuser import (
    AcquirersCallback, AcquirersListCallback, ConfirmDeleteAcquirerCallback, DeleteAcquirerCallback, MainPageCallback,
    NewAcquirerCallback)
from bot.states.superuser import NewAcquirerState
from models.acquirer import Acquirer

router = Router()


@router.callback_query(AcquirersCallback.filter())
async def acquirers_handlers(query: CallbackQuery, callback_data: AcquirersCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.ACCOUNTS,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Новый покупатель', callback_data=NewAcquirerCallback().pack()),
            ],
            [
                InlineKeyboardButton(text='Список покупателей', callback_data=AcquirersListCallback().pack()),
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack()),
            ],
        ])
    )


@router.callback_query(NewAcquirerCallback.filter())
async def new_acquirer_handlers(query: CallbackQuery, callback_data: NewAcquirerCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.ASK_ACQUIRER_NAME,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=AcquirersCallback().pack()),
            ],
        ])
    )
    await state.clear()
    await state.update_data(init_message_id=message.message_id)
    await state.set_state(NewAcquirerState.name)


@router.message(NewAcquirerState.name, F.text)
async def acquirer_name_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    acquirer = Acquirer(name=message.text)  # type: ignore
    acquirer.save()

    data = await state.get_data()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get('init_message_id'),
        text=messages.SUCCESSFUL_CREATE_ACQUIRER.format(name=acquirer.name),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=AcquirersCallback().pack()),
            ],
        ])
    )
    await state.clear()


@router.callback_query(AcquirersListCallback.filter())
async def acquirers_list_handlers(query: CallbackQuery, callback_data: AcquirersListCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    acquirers = Acquirer.query(Acquirer.deleted == False)  # type: ignore

    await message.edit_text(
        messages.ACQUIRERS_LIST,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'❌ {acquirer.name}',
                    callback_data=DeleteAcquirerCallback(acquirer_key=acquirer.key).pack()
                ),
            ]
            for acquirer in acquirers if acquirer.key
        ] + [
            [
                InlineKeyboardButton(text='Назад', callback_data=AcquirersCallback().pack()),
            ]
        ])
    )


@router.callback_query(DeleteAcquirerCallback.filter())
async def delete_acquirer_handlers(query: CallbackQuery, callback_data: DeleteAcquirerCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    acquirer = Acquirer.get_or_none(callback_data.acquirer_key)
    if not acquirer:
        return

    await message.edit_text(
        messages.ASK_CONFIRM_DELETE_ACQUIRER,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да',
                    callback_data=ConfirmDeleteAcquirerCallback(acquirer_key=acquirer.key).pack()
                ),
                InlineKeyboardButton(
                    text='Нет',
                    callback_data=AcquirersListCallback().pack()
                ),
            ],
        ])
    )


@router.callback_query(ConfirmDeleteAcquirerCallback.filter())
async def confirm_delete_acquirer_handlers(query: CallbackQuery, callback_data: ConfirmDeleteAcquirerCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    acquirer = Acquirer.get_or_none(callback_data.acquirer_key)
    if not acquirer:
        return

    acquirer.deleted = True
    acquirer.save()

    await message.edit_text(
        messages.SUCCESSFUL_DELETE_ACQUIRER,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=AcquirersListCallback().pack()),
            ],
        ])
    )
