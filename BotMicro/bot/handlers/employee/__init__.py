from aiogram import Router

from . import main_page, new_purchase, hide_purchase, new_fueling, new_dispatch, hide_dispatch
from . greeting import greet


router = Router()
router.include_router(main_page.router)
router.include_router(new_purchase.router)
router.include_router(hide_purchase.router)
router.include_router(new_fueling.router)
router.include_router(new_dispatch.router)
router.include_router(hide_dispatch.router)
