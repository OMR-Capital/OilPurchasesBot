from aiogram import Router

from .admin import router as admin_router
from .common import router as common_router
from .employee import router as employee_router
from .superuser import router as superuser_router


router = Router()
router.include_router(admin_router)
router.include_router(common_router)
router.include_router(employee_router)
router.include_router(superuser_router)

