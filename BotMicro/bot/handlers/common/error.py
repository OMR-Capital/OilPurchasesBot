import logging
from aiogram import Router
from aiogram.types.error_event import ErrorEvent

router = Router()


@router.errors()
async def errors_handler(event: ErrorEvent):
    logging.warning(event)
    return event
