import logging
from os import getenv

from deta import App  # type: ignore
from deta import Deta  # type: ignore

from bot.factory import create_bot, create_dispatcher
from web.factory import create_app

BOT_TOKEN = getenv('BOT_TOKEN', '')
TELEGRAM_SECRET = getenv('TELEGRAM_SECRET', '')


logging.basicConfig(level=logging.DEBUG)

deta = Deta()

bot = create_bot(token=BOT_TOKEN)
dispatcher = create_dispatcher(deta=deta)


app = create_app(
    deta=deta,
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=TELEGRAM_SECRET,
)
