from bot import messages
from bot.handlers.utils import edit_message
from models import User

from .main_page import open_main_page


async def greet(chat_id: int, init_message_id: int, user: User):
    msg = await edit_message(chat_id, init_message_id, messages.LOAD_PAGE)
    if msg:
        await open_main_page(msg)