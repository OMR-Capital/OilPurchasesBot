from aiogram import Router

from . import main_page, new_purchase, hide_purchase
from .greeting import greet

router = Router()
router.include_router(main_page.router)
router.include_router(new_purchase.router)
router.include_router(hide_purchase.router)