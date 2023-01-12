from aiogram import Router

from . import main_page, approve_purchase, statistic
from . greeting import greet

router = Router()
router.include_router(main_page.router)
router.include_router(approve_purchase.router)
router.include_router(statistic.router)
