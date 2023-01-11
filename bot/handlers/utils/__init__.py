from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message


async def edit_message(
    chat_id: int, 
    message_id: int, 
    text: Optional[str], 
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> Optional[Message]:
    bot = Bot.get_current()
    if bot is None:
        return

    if text is None:
        msg = await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup
        )
    else:
        msg = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup
        )
    
    return msg if isinstance(msg, Message) else None


async def get_init_message_id(state: FSMContext) -> Optional[int]:
    data = await state.get_data()
    return data.get('init_message_id')