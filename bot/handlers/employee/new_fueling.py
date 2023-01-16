from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from bot import messages
from bot.callbacks.employee import MainPageCallback, NewFuelingCallback
from bot.handlers.utils.chat import error
from bot.handlers.utils.fueling import new_fueling
from statistic import update_fuelings_statistic

router = Router()


@router.callback_query(NewFuelingCallback.filter())
async def new_fueling_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.clear()

    message = query.message
    if not message:
        return
    
    fueling = await new_fueling(message)
    if not fueling:
        await error(message.chat.id, message.message_id, MainPageCallback().pack())

    await message.edit_text(
        messages.SUCCESSFUL_CREATE_FUELING,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Назад', callback_data=MainPageCallback().pack())]
        ])
    )

    update_fuelings_statistic()
