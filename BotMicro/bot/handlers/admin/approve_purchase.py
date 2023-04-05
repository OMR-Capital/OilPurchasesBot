from aiogram import Router
from aiogram.types import CallbackQuery, Message

from bot import messages
from bot.callbacks.admin import ApprovePurchaseCallback
from bot.handlers.utils.purchases import approve_purchase

router = Router()


@router.callback_query(ApprovePurchaseCallback.filter())
async def approve_purchase_handler(query: CallbackQuery, message: Message, callback_data: ApprovePurchaseCallback):
    try:
        await approve_purchase(message, callback_data.purchase)
    except:
        await message.answer(messages.ERROR)

    try:
        await message.delete()
    except:
        pass
