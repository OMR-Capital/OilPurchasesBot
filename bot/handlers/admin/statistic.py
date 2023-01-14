from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from bot import messages
from bot.callbacks.admin import StatisticCallback
from bot.callbacks.superuser import MainPageCallback
from bot.handlers.utils.chat import error
from statistic import make_statistic, update_statistic_table

router = Router()


@router.callback_query(StatisticCallback.filter())
async def statistics_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.clear()

    message = query.message
    if not message:
        return

    await message.edit_text(messages.WAIT)

    statistics_data = make_statistic()
    url = update_statistic_table(statistics_data)

    if url is None:
        await error(message.chat.id, message.message_id, MainPageCallback().pack())
    else:
        await message.edit_text(
            messages.SUCCESSFUL_MAKE_STATISTIC,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Открыть', url=url)],
                [InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())],
            ])
        )
