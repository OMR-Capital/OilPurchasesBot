from aiogram import Router
from aiogram.types import CallbackQuery, Message

from bot.callbacks.admin import ApprovePurchaseCallback
from bot.handlers.utils.purchases import approve_purchase
from utils.statistic.purchases import update_purchase_stats

router = Router()


@router.callback_query(ApprovePurchaseCallback.filter())
async def approve_purchase_handler(query: CallbackQuery, message: Message, callback_data: ApprovePurchaseCallback):
    purchase = await approve_purchase(message, callback_data.purchase)
    if purchase is None:
        return
    
    try:
        await message.delete()
    except:
        pass
    
    await update_purchase_stats(purchase)
    