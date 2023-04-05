from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.employee import (MainPageCallback, NewDispatchCallback,
                                    NewFuelingCallback, NewPurchaseCallback)

router = Router()


@router.callback_query(MainPageCallback.filter())
async def main_page_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await state.clear()
    await open_main_page(message)


async def open_main_page(message: Message):
    await message.edit_text(
        messages.MAIN_PAGE,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Новая закупка', callback_data=NewPurchaseCallback().pack())],
            [InlineKeyboardButton(text='Новая отгрузка', callback_data=NewDispatchCallback().pack())],
            [InlineKeyboardButton(text='Заправка', callback_data=NewFuelingCallback().pack())],
        ])
    )
