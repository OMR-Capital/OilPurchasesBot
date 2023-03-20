from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def other_handler(message: Message):
    await message.delete()