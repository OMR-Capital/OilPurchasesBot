from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.employee import HidePurchaseCallback

router = Router()


@router.callback_query(HidePurchaseCallback.filter())
async def hide_purchase_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return
    
    await message.delete()