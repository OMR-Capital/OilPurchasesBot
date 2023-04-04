from fastapi import APIRouter

from .purchases import purchases_router

root_router = APIRouter()
root_router.include_router(purchases_router)
