from datetime import datetime, timedelta, timezone
from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import messages
from bot.callbacks.admin import ApprovePurchaseCallback
from bot.callbacks.employee import HidePurchaseCallback
from models import Purchase, User
from models.spread import Spread
from odetam.exceptions import ItemNotFound

TIMEZONE = timezone(timedelta(hours=3), name='Europe/Moscow')


async def new_purchase(message: Message, state: FSMContext) -> Optional[Purchase]:
    data = await state.get_data()

    result = User.query(User.chat_id == message.chat.id)
    if not result:
        return None

    creator = result.pop()

    try:
        purchase = Purchase(
            client_type='Менеджерский' if data.get('from_manager') else 'Собственный',
            contract_type='Безнал' if data.get('cashless') else 'Нал',
            inn=data.get('inn'),
            supplier=data.get('supplier'),
            amount=data.get('amount'),
            price=data.get('price'),
            card=data.get('card'),
            bank=data.get('bank'),
            approved=False,
            creator=creator.key,
            create_time=datetime.now()
        )
        purchase.save()
    except:
        return None
    else:
        await spread_purchase(purchase, creator)
        
    return purchase


async def spread_purchase(purchase: Purchase, creator: User):
    bot = Bot.get_current()
    if not bot:
        return

    spread = Spread(key=purchase.key, messages=[])
    admins = User.query((User.mode == 'admin') | (
        User.mode == 'superuser'))  # type: ignore
    for admin in admins:
        try:
            create_time = purchase.create_time.astimezone(TIMEZONE)

            msg = await bot.send_message(
                admin.chat_id or 0,
                messages.PURCHASE_NOTIFICATION.format(
                    creator=creator.name,
                    time=create_time.isoformat(sep=' ', timespec='minutes'),
                    inn=purchase.inn,
                    contract_type=purchase.contract_type,
                    client_type=purchase.client_type,
                    supplier=purchase.supplier,
                    amount=purchase.amount,
                    price=purchase.price,
                    card=purchase.card,
                    bank=purchase.bank,
                    full_price=purchase.amount * purchase.price
                ),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='Подтвердить',
                            callback_data=ApprovePurchaseCallback(
                                purchase=(purchase.key or '')
                            ).pack()
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
            creator.chat_id or 0,
            messages.PURCHASE_APPROVED.format(
                approver=approver.name,
                contract_type=purchase.contract_type,
                client_type=purchase.client_type,
                inn=purchase.inn,
                supplier=purchase.supplier,
                amount=purchase.amount,
                price=purchase.price,
                card=purchase.card,
                bank=purchase.bank,
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

    try:
        spread = Spread.get(purchase.key)
        for chat_id, message_id in spread.messages:
            try:
                await bot.delete_message(chat_id, message_id)
            except:
                pass
        spread.delete()
    except ItemNotFound:
        pass

    purchase.save()
    return purchase
