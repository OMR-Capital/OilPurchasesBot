from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import messages
from bot.callbacks.employee import HideDispatchCallback
from models.dispatch import Dispatch
from models.user import User
from utils.datetime import MSC_TZ


async def new_dispatch(message: Message, bot: Bot, state: FSMContext) -> Optional[Dispatch]:
    data = await state.get_data()

    result = User.query((User.chat_id == message.chat.id) & (User.mode == 'employee'))
    if not result:
        return None

    creator = result.pop()
    amount = float(data.get('amount', 0))
    dispatch = Dispatch(
        creator=creator.name,
        create_time=datetime.now(),
        destination=data['destination'],
        amount=amount,
        area=creator.area
    )
    dispatch.save()

    await spread_dispatch(dispatch, creator, bot)
    return dispatch


async def spread_dispatch(dispatch: Dispatch, creator: User, bot: Bot):
    admins = User.query((User.mode == 'admin') | (User.mode == 'superuser'))  # type: ignore
    for admin in admins:
        try:
            create_time = dispatch.create_time.astimezone(MSC_TZ)

            await bot.send_message(
                chat_id=admin.chat_id or 0,
                text=messages.DISPATCH_NOTIFICATION.format(
                    creator=creator.name,
                    time=create_time.isoformat(sep=' ', timespec='minutes'),
                    area=dispatch.area,
                    amount=dispatch.amount,
                    destination=dispatch.destination,
                ),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='Скрыть',
                            callback_data=HideDispatchCallback().pack()
                        )
                    ]
                ])
            )
        except:
            pass
