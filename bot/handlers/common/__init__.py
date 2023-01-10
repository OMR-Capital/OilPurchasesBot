from aiogram import Router

from . import start, login

router = Router()
router.include_router(start.router)
router.include_router(login.router)