import logging
from time import time
from typing import Any, Optional
from fastapi import APIRouter
from models.purchase import Purchase

from models.user import User
from utils.micro_api.requests import request_micro
from utils.statistic.purchases import add_purchase_stats


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


@develop_router.post('/update_stats')
async def update_stats():
    st = time()

    purchases = Purchase.get_all()

    result = await request_micro(
        method='GET',
        micro='statistic',
        route='/purchase'
    )
    purchases_stats = result['purchases']
    stats_keys = set([purchase['key'] for purchase in purchases_stats])

    not_processed: list[Purchase] = []
    for purchase in purchases:
        if purchase.key not in stats_keys:
            not_processed.append(purchase)

    results: list[Optional[dict[str, Any]]] = []
    for purchase in not_processed:
        if time() - st > 15:
            return {'processed': len(results), 'left': len(purchases) - len(stats_keys), 'results': results}

        try:
            result = await add_purchase_stats(purchase)
            results.append(result)
        except Exception as e:
            logger = logging.getLogger('bot')
            logger.exception(e)
            logger.warning(f'Failed to update purchase {purchase.key}')
            results.append(None)

    return None
