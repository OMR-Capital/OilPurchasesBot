from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from bot import messages
from bot.callbacks.employee import (FuelingCostCallback, MainPageCallback,
                                    NewFuelingCallback)
from bot.handlers.utils.chat import error
from bot.handlers.utils.fueling import new_fueling
from bot.handlers.utils.message_edit import edit_message, get_init_message_id
from bot.states.employee import NewFueling
from statistic.fuelings_statistic import update_fuelings_statistic


router = Router()


@router.callback_query(NewFuelingCallback.filter())
async def new_fueling_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.clear()

    message = query.message
    if not message:
        return

    await message.edit_text(
        messages.ASK_FUELING_COST,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='500₽', callback_data=FuelingCostCallback(cost=500).pack())
            ],
            [
                InlineKeyboardButton(text='1000₽', callback_data=FuelingCostCallback(cost=1000).pack())
            ],
            [
                InlineKeyboardButton(text='1500₽', callback_data=FuelingCostCallback(cost=1500).pack())
            ],
            [
                InlineKeyboardButton(text='2000₽', callback_data=FuelingCostCallback(cost=2000).pack())
            ],
            [
                InlineKeyboardButton(text='Отмена', callback_data=MainPageCallback().pack())
            ]
        ])
    )
    await state.update_data(init_message_id=message.message_id)
    await state.set_state(NewFueling.cost)


@router.callback_query(FuelingCostCallback.filter(), NewFueling.cost)
async def fueling_cost_handler(query: CallbackQuery, state: FSMContext, callback_data: FuelingCostCallback):
    await query.answer()

    message = query.message
    if not message:
        return

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    fueling = await new_fueling(message, callback_data.cost)
    if not fueling:
        await error(message.chat.id, message.message_id, MainPageCallback().pack())
        return

    await edit_message(
        message.chat.id,
        init_message_id,
        messages.SUCCESSFUL_CREATE_FUELING,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())
            ]
        ])
    )

    await state.clear()
    update_fuelings_statistic()
