from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from bot.callbacks.employee import HidePurchaseCallback
from models.spread import Spread
from odetam.exceptions import ItemNotFound

from bot import messages
from bot.callbacks.admin import ApprovePurchaseCallback
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

    spread = Spread(purchase=purchase.key, messages=[])
    admins = User.query((User.mode == 'admin') | (User.mode == 'superuser')) # type: ignore
    for admin in admins:
        try:
            msg = await bot.send_message(
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
                            callback_data=ApprovePurchaseCallback(purchase=purchase.key).pack()
                        )
                    ]
                ])
            ) 
            spread.messages.append((msg.chat.id, msg.message_id))
        except:
            pass
            
    spread.save()


async def approve_purchase(message: Message, purchase_key: str) -> Optional[Purchase]:
    try:
        purchase = Purchase.get(purchase_key)
    except ItemNotFound:
        return

    if purchase.approved:
        return purchase

    result = User.query(User.chat_id == message.chat.id)
    if not result:
        return

    approver = result.pop()

    purchase.approved = True
    purchase.approver = approver.key
    purchase.approve_time = datetime.now()
    
    bot = Bot.get_current()
    if not bot:
        return

    try:
        creator = User.get(purchase.creator)
    except ItemNotFound:
        return

    try:
        await bot.send_message(
            creator.chat_id,
            messages.PURCHASE_APPROVED.format(
                approver=approver.name,
                supplier=purchase.supplier,
                amount=purchase.amount,
                price=purchase.price,
                card=purchase.card,        
            ),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Скрыть',
                        callback_data=HidePurchaseCallback().pack()
                    )
                ]
            ])
        )
    except:
        return

    result = Spread.query(Spread.purchase == purchase.key)
    if not result:
        return purchase
    
    spread = result.pop()
    for chat_id, message_id in spread.messages:
        try:
            await bot.delete_message(chat_id, message_id)
        except:
            pass

    purchase.save()
    return purchase

    
        
    