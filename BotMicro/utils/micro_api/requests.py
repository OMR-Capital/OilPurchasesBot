from os import getenv
from typing import Any, Optional

from aiohttp.client import ClientSession

from utils.micro_api.utils import escape_dict_strings

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "x-api-key": getenv('DETA_API_KEY', ''),
}

BASE_URL = f'https://{getenv("DETA_SPACE_APP_HOSTNAME")}'


def get_micro_route_url(micro_path: str, route: str) -> str:
    return f'{BASE_URL}/{micro_path}{route}'


async def request_micro(method: str, micro: str, route: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    if data is not None:
        data = escape_dict_strings(data)

    if route[0] != '/':
        raise ValueError('Route must start with /')

    async with ClientSession(headers=HEADERS) as session:
        async with session.request(
            method,
            get_micro_route_url(micro, route),
            json=data,
        ) as response:
            response = await response.json()
            return await response.json()
