from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callbacks.admin import ApprovePurchaseCallback
from bot.handlers.utils.purchases import approve_purchase
from statistic import update_purchases_statistic

router = Router()


@router.callback_query(ApprovePurchaseCallback.filter())
async def approve_purchase_handler(query: CallbackQuery, callback_data: ApprovePurchaseCallback):
    await query.answer()

    message = query.message
    if not message:
        return

    await approve_purchase(message, callback_data.purchase)
    update_purchases_statistic()
