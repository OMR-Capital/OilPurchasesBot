from aiogram import Bot, Dispatcher
from aiogram_deta.storage import DetaStorage
from deta import Deta  # type: ignore

from bot import routing


def create_dispatcher(deta: Deta) -> Dispatcher:
    storage = DetaStorage(deta_base=deta.AsyncBase('fsm'))
    dispatcher = Dispatcher(storage=storage)

    routing.register_handlers(dispatcher)

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode='HTML')
