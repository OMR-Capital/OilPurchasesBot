from aiogram import Router

from . import main_page, accounts, new_admin
from .greeting import greet

router = Router()
router.include_router(main_page.router)
router.include_router(accounts.router)
router.include_router(new_admin.router)
