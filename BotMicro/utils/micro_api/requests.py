from os import getenv
from typing import Any, Optional

from aiohttp.client import ClientSession

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "x-api-key": getenv('DETA_API_KEY'),
}

BASE_URL = f'https://{getenv("DETA_SPACE_APP_HOSTNAME")}'


def get_micro_route_url(micro_path: str, route: str) -> str:
    return  f'{BASE_URL}/{micro_path}{route}'


async def request_micro(method: str, micro: str, route: str, data: Optional[str] = None) -> dict[str, Any]:
    if route[0] != '/':
        raise ValueError('Route must start with /')
    
    async with ClientSession() as session:
        async with session.request(
            method,
            get_micro_route_url(micro, route),
            data=data, 
            headers=HEADERS
        ) as response:
            return await response.json()
