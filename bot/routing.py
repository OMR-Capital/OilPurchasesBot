from aiogram import Dispatcher
from bot.handlers import common, admin, employee

def register_handlers(dispatcher: Dispatcher):
    dispatcher.include_router(common.router)
    dispatcher.include_router(admin.router)
    dispatcher.include_router(employee.router)