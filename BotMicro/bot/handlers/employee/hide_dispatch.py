from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.employee import HideDispatchCallback

router = Router()


@router.callback_query(HideDispatchCallback.filter())
async def hide_dispatch_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()

    message = query.message
    if not message:
        return
    
    await message.delete()