import logging
from aiogram import Router
from aiogram.types.error_event import ErrorEvent

router = Router()


@router.errors()
async def errors_handler(event: ErrorEvent):
    logger = logging.getLogger(__name__)
    logger.warning(event)
    return event
