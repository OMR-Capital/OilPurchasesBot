from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.employee import MainPageCallback, NewDispatchCallback, NewFuelingCallback, NewPurchaseCallback
from bot import messages

router = Router()


@router.callback_query(MainPageCallback.filter())
async def main_page_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.clear()
    
    message = query.message
    if not message:
        return

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

