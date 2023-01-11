from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import messages
from models import Purchase, User


async def new_purchase(message: Message, state: FSMContext) -> Optional[Purchase]:
    data = await state.get_data()

    result = User.query(User.chat_id == message.chat.id)
    if not result:
        return None
    
    creator = result.pop()

    purchase = Purchase(
        supplier=data.get('supplier'),
        amount=data.get('amount'),
        price=data.get('price'),
        card=data.get('card'),
        approved=False,
        creator=creator.key,
        create_time=datetime.now()
    )
    purchase.save()

    await spread_purchase(purchase, creator)

    return purchase
    

async def spread_purchase(purchase: Purchase, creator: User):
    bot = Bot.get_current()
    if not bot:
        return

    admins = User.query((User.mode == 'admin') | (User.mode == 'superuser'))
    for admin in admins:
        try:
            await bot.send_message(
                admin.chat_id or 0,
                messages.PURCHASE.format(
                    creator=creator.name,
                    time=purchase.create_time.isoformat(sep=' ', timespec='minutes'),
                    supplier=purchase.supplier,
                    amount=purchase.amount,
                    price=purchase.price,
                    card=purchase.card,        
                ),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='Подтвердить',
                            callback_data='test'
                        )
                    ]
                ])
            ) 
        except:
            pass