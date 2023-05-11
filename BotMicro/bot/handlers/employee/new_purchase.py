from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.employee import (ClientTypeCallback, ContractTypeCallback,
                                    MainPageCallback, NewPurchaseCallback,
                                    UnitCallback)
from bot.handlers.utils import edit_message, get_init_message_id
from bot.handlers.utils.purchases import new_purchase
from bot.states.employee import NewPurchaseState
from utils.statistic.purchases import add_purchase_stats

router = Router()

cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='Отмена', callback_data=MainPageCallback().pack())]
])


@router.callback_query(NewPurchaseCallback.filter())
async def new_purchase_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await message.edit_text(
        messages.ASK_CONTRACT_TYPE,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Безнал', callback_data=ContractTypeCallback(cashless=True).pack()),
                InlineKeyboardButton(text='Нал', callback_data=ContractTypeCallback(cashless=False).pack())
            ],
        ] + cancel_kb.inline_keyboard
        )
    )
    await state.update_data(init_message_id=message.message_id)
    await state.set_state(NewPurchaseState.contract_type)


@router.callback_query(NewPurchaseState.contract_type, ContractTypeCallback.filter())
async def contract_type_handler(query: CallbackQuery, message: Message, callback_data: ContractTypeCallback, state: FSMContext):
    await message.edit_text(
        messages.ASK_CLIENT_TYPE,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Менеджерский', callback_data=ClientTypeCallback(from_manager=True).pack()),
                InlineKeyboardButton(text='Собственный', callback_data=ClientTypeCallback(from_manager=False).pack())
            ],
        ] + cancel_kb.inline_keyboard
        )
    )
    await state.update_data(cashless=callback_data.cashless)
    await state.set_state(NewPurchaseState.client_type)


@router.callback_query(NewPurchaseState.client_type, ClientTypeCallback.filter())
async def client_type_handler(query: CallbackQuery, message: Message, callback_data: ClientTypeCallback, state: FSMContext):
    await message.edit_text(
        messages.ASK_SUPPLIER,
        reply_markup=cancel_kb
    )

    await state.update_data(from_manager=callback_data.from_manager)
    await state.set_state(NewPurchaseState.supplier)


@router.message(NewPurchaseState.supplier, F.text)
async def supplier_handler(message: Message, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    supplier = message.text or ''
    await state.update_data(supplier=supplier)

    await edit_message(
        message.chat.id,
        init_message_id,
        messages.ASK_UNIT,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Литры', callback_data=UnitCallback(unit='liter').pack()),
                InlineKeyboardButton(text='Килограммы', callback_data=UnitCallback(unit='kg').pack())
            ],
        ] + cancel_kb.inline_keyboard)
    )
    await state.set_state(NewPurchaseState.unit)


@router.callback_query(NewPurchaseState.unit, UnitCallback.filter())
async def unit_handler(query: CallbackQuery, message: Message, callback_data: UnitCallback, state: FSMContext):
    await message.edit_text(
        messages.ask_amount(callback_data.unit),
        reply_markup=cancel_kb
    )

    await state.update_data(unit=callback_data.unit)
    await state.set_state(NewPurchaseState.amount)


@router.message(NewPurchaseState.amount, F.text.regexp(r'^\d+\.?\d*$'))
async def amount_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    amount = message.text or ''
    await state.update_data(amount=amount)

    data = await state.get_data()
    if data.get('cashless'):
        await state.update_data(price=0, card='', bank='')
        await create_new_purchase(message, bot, state)
        return

    await edit_message(
        message.chat.id,
        init_message_id,
        messages.ask_price(data['unit']),
        cancel_kb
    )
    await state.set_state(NewPurchaseState.price)


@router.message(NewPurchaseState.amount, F.text)
async def wrong_amount_handler(message: Message, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await edit_message(message.chat.id, init_message_id, messages.WRONG_INTEGER, cancel_kb)


@router.message(NewPurchaseState.price, F.text.regexp(r'^\d+\.?\d*$'))
async def price_handler(message: Message, state: FSMContext):
    await message.delete()

    price = message.text or ''

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await edit_message(message.chat.id, init_message_id, messages.ASK_CARD, cancel_kb)

    await state.update_data(price=price)
    await state.set_state(NewPurchaseState.card)


@router.message(NewPurchaseState.price, F.text)
async def wrong_price_handler(message: Message, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    await edit_message(message.chat.id, init_message_id, messages.WRONG_INTEGER, cancel_kb)


@router.message(NewPurchaseState.card, F.text)
async def card_handler(message: Message, state: FSMContext):
    await message.delete()

    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    card = message.text or ''
    await state.update_data(card=card)

    await edit_message(message.chat.id, init_message_id, messages.ASK_BANK, cancel_kb)
    await state.set_state(NewPurchaseState.bank)


@router.message(NewPurchaseState.bank, F.text)
async def bank_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    bank = message.text or ''
    await state.update_data(bank=bank)
    await create_new_purchase(message, bot, state)


async def create_new_purchase(message: Message, bot: Bot, state: FSMContext):
    init_message_id = await get_init_message_id(state)
    if not init_message_id:
        return

    purchase = await new_purchase(message, state)
    if purchase is None:
        await message.answer(messages.ERROR)
        return

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=init_message_id,
        text=messages.SUCCESSFUL_CREATE_PURCHASE.format(
            contract_type=purchase.contract_type,
            client_type=purchase.client_type,
            supplier=purchase.supplier,
            amount=purchase.amount,
            price=purchase.price,
            card=purchase.card,
            bank=purchase.bank,
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data=MainPageCallback().pack())]
        ])
    )
    await state.clear()

    await add_purchase_stats(purchase)
