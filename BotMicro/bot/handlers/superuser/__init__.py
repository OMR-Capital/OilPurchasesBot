from aiogram import Router

from .accounts import router as accounts_router
from .accounts_list import router as accounts_list_router
from .acquirers import router as acquirers_router
from .amount_statistic import router as amount_statistic_router
from .edit_purchase import router as edit_purchase_router
from .greeting import greet  # it's magic, don't touch it
from .main_page import router as main_page_router
from .new_user import router as new_user_router
from .user_info import router as user_info_router

router = Router()
router.include_router(main_page_router)
router.include_router(accounts_router)
router.include_router(new_user_router)
router.include_router(accounts_list_router)
router.include_router(user_info_router)
router.include_router(amount_statistic_router)
router.include_router(acquirers_router)
router.include_router(edit_purchase_router)
