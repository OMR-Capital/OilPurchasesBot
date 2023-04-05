from os import getenv

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.admin import MainPageCallback
from bot.callbacks.superuser import AmountStatisticsCallback

router = Router()


@router.callback_query(MainPageCallback.filter())
async def main_page_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await state.clear()
    await open_main_page(message)


async def open_main_page(message: Message):
    await message.edit_text(
        messages.MAIN_PAGE,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Статистика', url=getenv('GOOGLE_SHEET_LINK', ''))],
            [InlineKeyboardButton(text='Статистика объемов', callback_data=AmountStatisticsCallback(user_mode='admin').pack())],
        ])
    )
