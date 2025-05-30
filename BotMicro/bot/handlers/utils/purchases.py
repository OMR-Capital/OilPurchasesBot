from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import messages
from bot.callbacks.admin import ApprovePurchaseCallback
from bot.callbacks.employee import HidePurchaseCallback
from models import Purchase, User
from models.purchase import Unit
from models.spread import Spread
from odetam.exceptions import ItemNotFound
from models.user import UserMode

from utils.datetime import MSC_TZ


async def new_purchase(message: Message, state: FSMContext) -> Optional[Purchase]:
    data = await state.get_data()

    result = User.query(User.chat_id == message.chat.id)
    if not result:
        return None

    creator = result.pop()

    unit = data.get('unit')
    amount = float(data.get('amount', 0))
    price = float(data.get('price', 0))
    if unit == Unit.KG:
        price, amount = price / 0.88, amount / 0.88

    purchase = Purchase(
        client_type=data.get('client_type'),
        contract_type=data.get('contract_type'),
        supplier=data.get('supplier'),
        amount=amount,
        price=price,
        card=data.get('card'),
        bank=data.get('bank'),
        approved=False,
        creator=creator.key,
        create_time=datetime.now(),
        area=creator.area
    )
    purchase.save()

    await spread_purchase(purchase, creator)
    return purchase


async def spread_purchase(purchase: Purchase, creator: User):
    bot = Bot.get_current()
    if not bot:
        return

    spread = Spread(key=purchase.key, messages=[])
    admins = User.query((User.mode == UserMode.ADMIN) | (User.mode == UserMode.SUPERUSER))  # type: ignore
    for admin in admins:
        try:
            create_time = purchase.create_time.astimezone(MSC_TZ)

            msg = await bot.send_message(
                admin.chat_id or 0,
                messages.PURCHASE_NOTIFICATION.format(
                    creator=creator.name,
                    time=create_time.isoformat(sep=' ', timespec='minutes'),
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
                continue
    except ItemNotFound:
        pass
    else:
        spread.delete()

    purchase.save()
    return purchase
