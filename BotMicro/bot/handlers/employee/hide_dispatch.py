from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.employee import HideDispatchCallback

router = Router()


@router.callback_query(HideDispatchCallback.filter())
async def hide_dispatch_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await message.delete()
