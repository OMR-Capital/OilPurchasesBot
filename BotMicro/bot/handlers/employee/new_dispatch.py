from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.employee import (AcquirerCallback, ConfirmDispatchCallback,
                                    MainPageCallback, NewDispatchCallback,
                                    UnitCallback)
from bot.handlers.utils.chat import error
from bot.handlers.utils.dispatches import new_dispatch
from bot.handlers.utils.message_edit import get_init_message_id
from bot.states.employee import NewDispatchState
from models.acquirer import Acquirer
from models.purchase import Unit

router = Router()


@router.callback_query(NewDispatchCallback.filter())
async def new_dispatch_handler(query: CallbackQuery, message: Message, callback_data: NewDispatchCallback, bot: Bot, state: FSMContext):
    acquirers = Acquirer.query(Acquirer.deleted == False) # type: ignore

    await message.edit_text(
        messages.ASK_ACQUIRER,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=acquirer.name, callback_data=AcquirerCallback(acquirer_key=acquirer.key).pack())
            ] for acquirer in acquirers if acquirer.key
        ] + [
            [
                InlineKeyboardButton(text='Отмена', callback_data=MainPageCallback().pack())
            ]
        ])
    )
    await state.update_data(init_message_id=message.message_id)
    await state.set_state(NewDispatchState.acquirer)


@router.callback_query(NewDispatchState.acquirer, AcquirerCallback.filter())
async def acquirer_handler(query: CallbackQuery, message: Message, callback_data: AcquirerCallback, state: FSMContext):
    acquirer = Acquirer.get_or_none(callback_data.acquirer_key)
    if not acquirer:
        return

    await message.edit_text(
        text=messages.ASK_UNIT,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Литры', callback_data=UnitCallback(unit=Unit.LITERS).pack()),
                InlineKeyboardButton(text='Килограммы', callback_data=UnitCallback(unit=Unit.KG).pack())
            ],
        ] + [
            [
                InlineKeyboardButton(text='Отмена', callback_data=MainPageCallback().pack())
            ]
        ])
    )
    await state.update_data(acquirer_key=acquirer.key, acquirer_name=acquirer.name)
    await state.set_state(NewDispatchState.unit)


@router.callback_query(NewDispatchState.unit, UnitCallback.filter())
async def unit_handler(query: CallbackQuery, message: Message, callback_data: UnitCallback, state: FSMContext):
    await message.edit_text(
        messages.ask_amount(callback_data.unit),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())
            ]
        ])
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
    if data['unit'] == Unit.KG:
        amount = amount / 0.88

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=init_message_id,
        text=messages.DISPATCH_BASE.format(
            amount=amount,
            acquirer=data['acquirer_name']
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Подтвердить', callback_data=ConfirmDispatchCallback().pack())
            ]
        ] + [
            [
                InlineKeyboardButton(text='Отмена', callback_data=MainPageCallback().pack())
            ]
        ])
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
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())
            ]
        ])
    )


@router.callback_query(NewDispatchState.confirm, ConfirmDispatchCallback.filter())
async def confirm_handler(query: CallbackQuery, message: Message, callback_data: ConfirmDispatchCallback, bot: Bot, state: FSMContext):
    await create_new_dispatch(message, bot, state)
    await state.clear()


async def create_new_dispatch(message: Message, bot: Bot, state: FSMContext):
    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    data = await state.get_data()

    dispatch = await new_dispatch(message, bot, state)
    if dispatch is None:
        await error(message.chat.id, init_message_id, MainPageCallback().pack())
        return

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=init_message_id,
        text=messages.SUCCESSFUL_CREATE_DISPATCH.format(
            amount=dispatch.amount,
            acquirer=data['acquirer_name'],
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())
            ]
        ])
    )
    await state.clear()
