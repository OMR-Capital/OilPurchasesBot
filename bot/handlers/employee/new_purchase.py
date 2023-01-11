from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.employee import MainPageCallback, NewPurchaseCallback
from bot.handlers.utils import edit_message, get_init_message_id
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
    supplier = message.text or ''

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await edit_message(message.chat.id, init_message_id, messages.ASK_AMOUNT)
    
    await state.update_data(supplier=supplier)
    await state.set_state(NewPurchaseState.amount)