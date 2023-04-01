from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.employee import (ConfirmDispatchCallback, MainPageCallback,
                                    DestinationCallback, NewDispatchCallback, UnitCallback)
from bot.handlers.utils.chat import error
from bot.handlers.utils.dispatches import new_dispatch
from bot.handlers.utils.message_edit import get_init_message_id
from bot.states.employee import NewDispatchState

router = Router()


cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='Отмена', callback_data=MainPageCallback().pack())]
])


@router.callback_query(NewDispatchCallback.filter())
async def new_dispatch_handler(query: CallbackQuery,  callback_data: NewDispatchCallback, bot: Bot, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.ASK_DESTINATION,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Склад Саратов', callback_data=DestinationCallback(destination='Склад Саратов').pack()),
                InlineKeyboardButton(text='ООО "СПС"', callback_data=DestinationCallback(destination='ООО "СПС"').pack()),
                InlineKeyboardButton(text='ООО "НПО "ХимБурНефть"', callback_data=DestinationCallback(destination='ООО "НПО "ХимБурНефть"').pack()),
                InlineKeyboardButton(text='ООО "СпецАвтомат"', callback_data=DestinationCallback(destination='ООО "СпецАвтомат"').pack()),
            ],
        ] + cancel_kb.inline_keyboard
        )
    )
    await state.update_data(init_message_id=message.message_id)
    await state.set_state(NewDispatchState.destination)


@router.callback_query(NewDispatchState.destination, DestinationCallback.filter())
async def destination_handler(query: CallbackQuery, callback_data: DestinationCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        text=messages.ASK_UNIT,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Литры', callback_data=UnitCallback(unit='liter').pack()),
                InlineKeyboardButton(text='Килограммы', callback_data=UnitCallback(unit='kg').pack())
            ],
        ] + cancel_kb.inline_keyboard)
    )
    await state.update_data(destination=callback_data.destination)
    await state.set_state(NewDispatchState.unit)



@router.callback_query(NewDispatchState.unit, UnitCallback.filter())
async def unit_handler(query: CallbackQuery, callback_data: UnitCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.ask_amount(callback_data.unit),
        reply_markup=cancel_kb
    )
    await state.update_data(unit=callback_data.unit)
    await state.set_state(NewDispatchState.amount)


@router.message(NewDispatchState.amount, F.text.regexp(r'^\d+\.?\d*$'))
async def amount_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    data = await state.get_data()
    amount = float(message.text or '')
    if data['unit'] == 'kg':
        amount = amount / 0.88

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=init_message_id,
        text=messages.DISPATCH_BASE.format(
            amount=amount,
            destination=data['destination']
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Подтвердить', callback_data=ConfirmDispatchCallback().pack())
            ]
        ] + cancel_kb.inline_keyboard)
    )
    await state.update_data(amount=amount)
    await state.set_state(NewDispatchState.confirm)


@router.message(NewDispatchState.amount, F.text)
async def wrong_amount_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=init_message_id,
        text=messages.WRONG_INTEGER,
        reply_markup=cancel_kb
    )


@router.callback_query(NewDispatchState.confirm, ConfirmDispatchCallback.filter())
async def confirm_handler(query: CallbackQuery, callback_data: ConfirmDispatchCallback, bot: Bot, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await create_new_dispatch(message, bot, state)
    await state.clear()


async def create_new_dispatch(message: Message, bot: Bot, state: FSMContext):
    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    dispatch = await new_dispatch(message, bot, state)
    if dispatch is None:
        await error(message.chat.id, init_message_id, MainPageCallback().pack())
        return

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=init_message_id,
        text=messages.SUCCESSFUL_CREATE_DISPATCH.format(
            amount=dispatch.amount,
            destination=dispatch.destination,
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())
            ]
        ])
    )
    await state.clear()
