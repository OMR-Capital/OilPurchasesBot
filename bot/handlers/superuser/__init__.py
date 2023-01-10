from aiogram import Router

from . import main_page, accounts
from .greeting import greet

router = Router()
router.include_router(main_page.router)
router.include_router(accounts.router)
