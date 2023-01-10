from aiogram.types import Message

from bot import messages
from models import User

from .main_page import open_main_page


async def greet(message: Message, user: User):
    await message.answer(
        messages.SUCCESSFUL_ADMIN_LOGIN.format(name=user.name)
    )
    msg = await message.answer(messages.LOAD_PAGE)
    await msg.pin(disable_notification=True)
    await open_main_page(msg)