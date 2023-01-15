from aiogram import Router

from . import start, login, backdoor, logout

router = Router()
router.include_router(start.router)
router.include_router(login.router)
router.include_router(logout.router)
router.include_router(backdoor.router)