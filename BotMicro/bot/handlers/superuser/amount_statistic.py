from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from bot.callbacks.superuser import AmountStatisticsCallback, MainPageCallback
from bot.messages import amount_statistics
from models.dispatch import Dispatch
from models.purchase import Purchase

router = Router()


@router.callback_query(AmountStatisticsCallback.filter())
async def amount_statistic_handler(query: CallbackQuery, callback_data: AmountStatisticsCallback, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return

    purchases = Purchase.query(Purchase.approved == True)

    areas = set(purchase.area for purchase in purchases if purchase.area)
    area_to_purchases = {
        area: [purchase for purchase in purchases if purchase.area == area]
        for area in areas
    }

    dispatches = Dispatch.get_all()
    area_to_dispatches = {
        area: [dispatch for dispatch in dispatches if dispatch.area == area]
        for area in areas
    }

    total_purchased_amount = sum(purchase.amount for purchase in purchases)
    total_dispatched_amount = sum(dispatch.amount for dispatch in dispatches) * 0.88
    areas_amount = {
        area: sum(purchase.amount for purchase in area_to_purchases[area]) -
        sum(dispatch.amount for dispatch in area_to_dispatches[area]) for area in areas}

    await message.edit_text(
        text=amount_statistics(
            total_purchased_amount,
            total_dispatched_amount,
            areas_amount
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())]
        ])
    )
