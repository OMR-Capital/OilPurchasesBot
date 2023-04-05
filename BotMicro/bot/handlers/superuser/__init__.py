from aiogram import Router

from . import (accounts, accounts_list, acquirers, amount_statistic, main_page,
               new_user, user_info)
from .greeting import greet

router = Router()
router.include_router(main_page.router)
router.include_router(accounts.router)
router.include_router(new_user.router)
router.include_router(accounts_list.router)
router.include_router(user_info.router)
router.include_router(amount_statistic.router)
router.include_router(acquirers.router)
