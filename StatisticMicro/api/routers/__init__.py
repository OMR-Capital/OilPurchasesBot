from fastapi import APIRouter

from .applications import applications_router


root_router = APIRouter()
root_router.include_router(applications_router)
