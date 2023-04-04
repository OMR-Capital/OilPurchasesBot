import logging
from fastapi import APIRouter
from models.purchase import Purchase

from models.user import User


develop_router = APIRouter(prefix='/develop', tags=['Develop'])


@develop_router.post('/update_users')
async def update_users():
    users = User.get_all()
    User.put_many(users)


@develop_router.post('/update_purchases')
async def update_purchases():
    logger = logging.getLogger('bot')
    logger.warning('Test')
    purchases = Purchase.get_all()
    Purchase.put_many(purchases)
