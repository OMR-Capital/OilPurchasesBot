from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.employee import MainPageCallback, NewPurchaseCallback
from bot.handlers.utils.chat import error
from bot.handlers.utils import edit_message, get_init_message_id
from bot.handlers.utils.purchases import new_purchase
from bot.states.employee import NewPurchaseState

router = Router()

cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data=MainPageCallback().pack())]
])


@router.callback_query(NewPurchaseCallback.filter())
async def new_purchase_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.ASK_SUPPLIER,
        reply_markup=cancel_kb
    )
    await state.update_data(init_message_id=message.message_id)
    await state.set_state(NewPurchaseState.supplier)


@router.message(NewPurchaseState.supplier, F.text)
async def supplier_handler(message: Message, state: FSMContext):
    await message.delete()

    supplier = message.text or ''

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await edit_message(message.chat.id, init_message_id, messages.ASK_AMOUNT, cancel_kb)
    
    await state.update_data(supplier=supplier)
    await state.set_state(NewPurchaseState.amount)



@router.message(NewPurchaseState.amount, F.text)
async def amount_handler(message: Message, state: FSMContext):
    await message.delete()
    
    amount = message.text or ''

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await edit_message(message.chat.id, init_message_id, messages.ASK_PRICE, cancel_kb)
    
    await state.update_data(amount=amount)
    await state.set_state(NewPurchaseState.price)



@router.message(NewPurchaseState.price, F.text)
async def price_handler(message: Message, state: FSMContext):
    await message.delete()
    
    price = message.text or ''

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await edit_message(message.chat.id, init_message_id, messages.ASK_CARD, cancel_kb)
    
    await state.update_data(price=price)
    await state.set_state(NewPurchaseState.card)


@router.message(NewPurchaseState.card, F.text)
async def card_handler(message: Message, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    card = message.text or ''
    await state.update_data(card=card)

    purchase = await new_purchase(message, state)
    if purchase is None:
        await error(message.chat.id, init_message_id, MainPageCallback().pack())
        return

    await edit_message(
        message.chat.id, 
        init_message_id, 
        messages.SUCCESSFUL_CREATE_PURCHASE.format(
            supplier=purchase.supplier,
            amount=purchase.amount,
            price=purchase.price,
            card=purchase.card,
        ),
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())]
        ])
    )
    await state.clear()
    