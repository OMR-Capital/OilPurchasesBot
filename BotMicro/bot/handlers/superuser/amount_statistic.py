from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot.callbacks.admin import MainPageCallback as admin_menu_callback
from bot.callbacks.superuser import AmountStatisticsCallback
from bot.callbacks.superuser import MainPageCallback as superuser_menu_callback
from bot.messages import amount_statistics
from models.dispatch import Dispatch
from models.purchase import Purchase
from models.user import UserMode

router = Router()


def get_areas_amount(
    areas: set[str],
    area_to_purchases: dict[str, list[Purchase]],
    area_to_dispatches: dict[str, list[Dispatch]]
) -> dict[str, float]:
    areas_amount: dict[str, float] = {}
    for area in areas:
        purchased_amount = sum(purchase.amount for purchase in area_to_purchases[area])
        dispatched_amount = sum(dispatch.amount for dispatch in area_to_dispatches[area])
        areas_amount[area] = purchased_amount - dispatched_amount

    return areas_amount


@router.callback_query(AmountStatisticsCallback.filter())
async def amount_statistic_handler(query: CallbackQuery, message: Message, callback_data: AmountStatisticsCallback, state: FSMContext):
    purchases = Purchase.query(Purchase.approved == True)  # type: ignore

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
    areas_amount = get_areas_amount(areas, area_to_purchases, area_to_dispatches)

    menu_callback = superuser_menu_callback if callback_data.user_mode == UserMode.SUPERUSER else admin_menu_callback
    await message.edit_text(
        text=amount_statistics(
            total_purchased_amount,
            total_dispatched_amount,
            areas_amount
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data=menu_callback().pack()
                )
            ]
        ])
    )
