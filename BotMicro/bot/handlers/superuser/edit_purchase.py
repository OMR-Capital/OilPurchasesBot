from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot import messages
from bot.callbacks.employee import (ClientTypeCallback, ContractTypeCallback,
                                    UnitCallback)
from bot.callbacks.superuser import (EditPurchaseCallback, EditSkipCallback,
                                     MainPageCallback)
from bot.states.superuser import EditPurchaseState
from models.purchase import ClientType, ContractType, Purchase, Unit

router = Router()


async def get_purchase(state: FSMContext) -> Purchase:
    data = await state.get_data()
    return Purchase._deserialize(data['purchase'])  # type: ignore


async def set_purchase(state: FSMContext, purchase: Purchase):
    await state.update_data(purchase=purchase._serialize())  # type: ignore


@router.callback_query(EditPurchaseCallback.filter())
async def edit_purchase_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await message.edit_text(
        messages.ASK_EDIT_PURCHASE_KEY,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Отмена',
                    callback_data=MainPageCallback().pack()
                )
            ]
        ])
    )
    await state.clear()
    await state.update_data(init_message_id=message.message_id)
    await state.set_state(EditPurchaseState.key)


@router.message(EditPurchaseState.key, F.text, F.text.as_('text'))
async def edit_purchase_key_handler(message: Message, text: str, bot: Bot, state: FSMContext):
    await message.delete()

    data = await state.get_data()

    purchase = Purchase.get_or_none(text)
    if not purchase:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data['init_message_id'],
            text=messages.PURCHASE_NOT_FOUND,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Отмена',
                        callback_data=MainPageCallback().pack()
                    )
                ]
            ])
        )
        await state.clear()
        return

    await set_purchase(state, purchase)
    await ask_contract_type(message, bot, state)


async def ask_contract_type(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    purchase = await get_purchase(state)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=messages.edit_purchase_ask(purchase, messages.ASK_CONTRACT_TYPE),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Безнал',
                    callback_data=ContractTypeCallback(contract_type=ContractType.CASHLESS).pack()
                ),
                InlineKeyboardButton(
                    text='Нал',
                    callback_data=ContractTypeCallback(contract_type=ContractType.CASH).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Отмена',
                    callback_data=MainPageCallback().pack()
                ),
                InlineKeyboardButton(
                    text='Пропустить 🔜',
                    callback_data=EditSkipCallback().pack()
                )
            ],
        ])
    )
    await state.set_state(EditPurchaseState.contract_type)


@router.callback_query(EditPurchaseState.contract_type, EditSkipCallback.filter())
async def skip_contract_type_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await ask_client_type(message, state)


@router.callback_query(EditPurchaseState.contract_type, ContractTypeCallback.filter())
async def contract_type_handler(query: CallbackQuery, message: Message, callback_data: ContractTypeCallback, state: FSMContext):
    purchase = await get_purchase(state)
    purchase.contract_type = callback_data.contract_type
    await set_purchase(state, purchase)

    await ask_client_type(message, state)


async def ask_client_type(message: Message, state: FSMContext):
    purchase = await get_purchase(state)
    await message.edit_text(
        messages.edit_purchase_ask(purchase, messages.ASK_CLIENT_TYPE),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Менеджерский',
                    callback_data=ClientTypeCallback(client_type=ClientType.MANAGER).pack()
                ),
                InlineKeyboardButton(
                    text='Собственный',
                    callback_data=ClientTypeCallback(client_type=ClientType.OWN).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Отмена',
                    callback_data=MainPageCallback().pack()
                ),
                InlineKeyboardButton(
                    text='Пропустить 🔜',
                    callback_data=EditSkipCallback().pack()
                )
            ],
        ])
    )
    await state.set_state(EditPurchaseState.client_type)


@router.callback_query(EditPurchaseState.client_type, EditSkipCallback.filter())
async def skip_client_type_handler(query: CallbackQuery, message: Message, state: FSMContext):
    await ask_supplier(message, state)


@router.callback_query(EditPurchaseState.client_type, ClientTypeCallback.filter())
async def client_type_handler(query: CallbackQuery, message: Message, callback_data: ClientTypeCallback, state: FSMContext):
    purchase = await get_purchase(state)
    purchase.client_type = callback_data.client_type
    await set_purchase(state, purchase)

    await ask_supplier(message, state)


async def ask_supplier(message: Message, state: FSMContext):
    purchase = await get_purchase(state)
    await message.edit_text(
        messages.edit_purchase_ask(purchase, messages.ASK_SUPPLIER),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Отмена',
                    callback_data=MainPageCallback().pack()
                ),
                InlineKeyboardButton(
                    text='Пропустить 🔜',
                    callback_data=EditSkipCallback().pack()
                )
            ]
        ])
    )
    await state.set_state(EditPurchaseState.supplier)


@router.callback_query(EditPurchaseState.supplier, EditSkipCallback.filter())
async def skip_supplier_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await ask_unit(message, bot, state)


@router.message(EditPurchaseState.supplier, F.text, F.text.as_('text'))
async def supplier_handler(message: Message, text: str, bot: Bot, state: FSMContext):
    await message.delete()

    purchase = await get_purchase(state)
    purchase.supplier = text
    await set_purchase(state, purchase)

    await ask_unit(message, bot, state)


async def ask_unit(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    purchase = await get_purchase(state)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=messages.edit_purchase_ask(purchase, messages.ASK_UNIT),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Литры',
                    callback_data=UnitCallback(unit=Unit.LITERS).pack()
                ),
                InlineKeyboardButton(
                    text='Килограммы',
                    callback_data=UnitCallback(unit=Unit.KG).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Отмена',
                    callback_data=MainPageCallback().pack()
                ),
                InlineKeyboardButton(
                    text='Пропустить 🔜',
                    callback_data=EditSkipCallback().pack()
                )
            ],
        ])
    )
    await state.set_state(EditPurchaseState.unit)


@router.callback_query(EditPurchaseState.unit, EditSkipCallback.filter())
async def skip_unit_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await ask_card(message, bot, state)


@router.callback_query(EditPurchaseState.unit, UnitCallback.filter())
async def unit_handler(query: CallbackQuery, message: Message, callback_data: UnitCallback, state: FSMContext):
    await state.update_data(unit=callback_data.unit)
    await ask_amount(message, state)


async def ask_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    purchase = await get_purchase(state)
    await message.edit_text(
        messages.edit_purchase_ask(
            purchase, messages.ask_amount(data['unit'])),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Отмена',
                    callback_data=MainPageCallback().pack()
                ),
                InlineKeyboardButton(
                    text='Пропустить 🔜',
                    callback_data=EditSkipCallback().pack()
                )
            ],
        ])
    )
    await state.set_state(EditPurchaseState.amount)


@router.callback_query(EditPurchaseState.amount, EditSkipCallback.filter())
async def skip_amount_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await ask_price(message, bot, state)


@router.message(EditPurchaseState.amount, F.text.regexp(r'^\d+\.?\d*$'), F.text.as_('text'))
async def amount_handler(message: Message, text: str, bot: Bot, state: FSMContext):
    await message.delete()

    purchase = await get_purchase(state)
    purchase.amount = float(text)
    await set_purchase(state, purchase)

    await ask_price(message, bot, state)


@router.message(EditPurchaseState.amount, F.text)
async def wrong_amount_handler(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(messages.WRONG_INTEGER)


async def ask_price(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    purchase = await get_purchase(state)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=messages.edit_purchase_ask(
            purchase, messages.ask_price(data['unit'])),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Отмена',
                    callback_data=MainPageCallback().pack()
                ),
                InlineKeyboardButton(
                    text='Пропустить 🔜',
                    callback_data=EditSkipCallback().pack()
                )
            ],
        ])
    )
    await state.set_state(EditPurchaseState.price)


@router.callback_query(EditPurchaseState.price, EditSkipCallback.filter())
async def skip_price_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await ask_card(message, bot, state)


@router.message(EditPurchaseState.price, F.text.regexp(r'^\d+\.?\d*$'), F.text.as_('text'))
async def price_handler(message: Message, text: str, bot: Bot, state: FSMContext):
    await message.delete()

    purchase = await get_purchase(state)
    purchase.price = float(text)
    await set_purchase(state, purchase)

    await ask_card(message, bot, state)


@router.message(EditPurchaseState.price, F.text)
async def wrong_price_handler(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(messages.WRONG_INTEGER)


async def ask_card(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    purchase = await get_purchase(state)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=messages.edit_purchase_ask(purchase, messages.ASK_CARD),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Отмена',
                    callback_data=MainPageCallback().pack()
                ),
                InlineKeyboardButton(
                    text='Пропустить 🔜',
                    callback_data=EditSkipCallback().pack()
                )
            ],
        ])
    )
    await state.set_state(EditPurchaseState.card)


@router.callback_query(EditPurchaseState.card, EditSkipCallback.filter())
async def skip_card_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await ask_bank(message, bot, state)


@router.message(EditPurchaseState.card, F.text, F.text.as_('text'))
async def card_handler(message: Message, text: str, bot: Bot, state: FSMContext):
    await message.delete()

    purchase = await get_purchase(state)
    purchase.card = text
    await set_purchase(state, purchase)

    await ask_bank(message, bot, state)


async def ask_bank(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    purchase = await get_purchase(state)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=messages.edit_purchase_ask(purchase, messages.ASK_BANK),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Отмена',
                    callback_data=MainPageCallback().pack()
                ),
                InlineKeyboardButton(
                    text='Пропустить 🔜',
                    callback_data=EditSkipCallback().pack()
                )
            ],
        ])
    )
    await state.set_state(EditPurchaseState.bank)


@router.callback_query(EditPurchaseState.bank, EditSkipCallback.filter())
async def skip_bank_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await update_purchase(message, bot, state)


@router.message(EditPurchaseState.bank, F.text, F.text.as_('text'))
async def bank_handler(message: Message, text: str, bot: Bot, state: FSMContext):
    await message.delete()

    purchase = await get_purchase(state)
    purchase.bank = text
    await set_purchase(state, purchase)

    await update_purchase(message, bot, state)


async def update_purchase(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    purchase = await get_purchase(state)
    purchase.save()

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['init_message_id'],
        text=messages.SUCCESSFUL_EDIT_PURCHASE,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Меню',
                    callback_data=MainPageCallback().pack()
                )
            ],
        ])
    )
    await state.clear()
    # await update_purchase_stats
