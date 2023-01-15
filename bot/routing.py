from aiogram import Dispatcher

from bot.handlers import admin, common, employee, superuser
from bot.handlers.common import other


def register_handlers(dispatcher: Dispatcher):
    dispatcher.include_router(common.router)
    dispatcher.include_router(admin.router)
    dispatcher.include_router(employee.router)
    dispatcher.include_router(superuser.router)
    dispatcher.include_router(other.router)
