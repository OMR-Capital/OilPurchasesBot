from aiogram import Router

from . import login

router = Router()
router.include_router(login.router)