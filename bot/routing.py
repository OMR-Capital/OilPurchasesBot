from aiogram import Dispatcher
from bot.handlers import common

def register_handlers(dispatcher: Dispatcher):
    dispatcher.include_router(common.router)