from aiogram import Bot, Dispatcher
from aiogram_deta.storage import DetaStorage
from deta import Deta  # type: ignore

from bot.handlers import router
from bot.middlewares.callback_answer import CallbackAnswerMiddleware
from bot.middlewares.callback_message import CallbackMessageMiddleware
from bot.middlewares.logging import LoggingMiddleware


def create_dispatcher(deta: Deta) -> Dispatcher:
    storage = DetaStorage(deta_base=deta.AsyncBase('fsm'))
    dispatcher = Dispatcher(storage=storage)

    dispatcher.include_router(router)

    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.callback_query.middleware(CallbackMessageMiddleware())
    
    dispatcher.update.middleware(LoggingMiddleware(60 * 60 * 2))

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode='HTML')
