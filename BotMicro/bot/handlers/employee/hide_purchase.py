from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.employee import HidePurchaseCallback

router = Router()


@router.callback_query(HidePurchaseCallback.filter())
async def hide_purchase_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await message.delete()
