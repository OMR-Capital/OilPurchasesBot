from aiogram.types import Message

from bot import messages
from models import User


async def greet(message: Message, user: User):
    await message.answer(
        messages.SUCCESSFUL_SUPERUSER_LOGIN.format(fullname=user.name)
    )