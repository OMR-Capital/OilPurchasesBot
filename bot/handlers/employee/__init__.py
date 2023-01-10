from aiogram import Router

from . import main_page
from .greeting import greet

router = Router()
router.include_router(main_page.router)