from os import getenv
from typing import Any

from deta import Deta  # type: ignore
from deta import App # type: ignore

from bot.factory import create_bot, create_dispatcher
from statistic.purchases_statistic import update_purchases_statistic
from web.factory import create_app

BOT_TOKEN = getenv('BOT_TOKEN', '')
TELEGRAM_SECRET = getenv('TELEGRAM_SECRET', '')


deta = Deta()

bot = create_bot(token=BOT_TOKEN)
dispatcher = create_dispatcher(deta=deta)


aiogram_app = create_app(
    deta=deta,
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=TELEGRAM_SECRET,
)
app = App(aiogram_app)


@app.lib.cron()
def update_statistic_handler(event: Any):
    update_purchases_statistic()
