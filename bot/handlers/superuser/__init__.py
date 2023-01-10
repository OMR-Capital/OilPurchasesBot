from aiogram import Router

from . import main_page, accounts, new_admin, new_employee, accounts_list, user_info
from .greeting import greet

router = Router()
router.include_router(main_page.router)
router.include_router(accounts.router)
router.include_router(new_admin.router)
router.include_router(new_employee.router)
router.include_router(accounts_list.router)
router.include_router(user_info.router)
