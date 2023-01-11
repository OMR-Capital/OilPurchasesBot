from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import messages
from bot.handlers.utils import edit_message


async def error(chat_id: int, init_message_id: int, callback_data: str):
    await edit_message(
        chat_id=chat_id,
        message_id=init_message_id,
        text=messages.ERROR,  
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data=callback_data)]
        ])
    )
