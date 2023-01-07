from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import messages
from bot.callbacks.admin import AdminLoginData
from bot.callbacks.employee import EmployeeLoginData

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        messages.START,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Администратор', callback_data=AdminLoginData().pack())],
            [InlineKeyboardButton(text='Работник', callback_data=EmployeeLoginData().pack())],
        ])
    )
