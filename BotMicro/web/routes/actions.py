from typing import Any
from fastapi import APIRouter

from statistic.purchases_statistic import update_purchases_statistic

actions_router = APIRouter(prefix='/__space/v0', tags=['Scheduled Actions'])


@actions_router.post('/actions')
async def handle_action(request: dict[str, Any]):
    if request.get('event', {}).get('id') == 'update_statistics':
        update_purchases_statistic()
