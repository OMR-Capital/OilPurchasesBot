import logging
from typing import Any
from fastapi import APIRouter

from statistic.purchases_statistic import update_purchases_statistic

actions_router = APIRouter(prefix='/__space/v0', tags=['Scheduled Actions'])


@actions_router.post('/actions')
async def handle_action(request: dict[str, Any]):
    logger = logging.getLogger(__name__)
    logger.warning(f'Action received: {request}')
    if request.get('event', {}).get('id') == 'update_statistics':
        update_purchases_statistic()
