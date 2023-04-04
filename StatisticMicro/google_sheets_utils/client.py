import json
from typing import Optional

from gspread.auth import service_account_from_dict # type: ignore
from gspread.client import Client


client: Optional[Client] = None


def init_client() -> None:
    global client

    if not client:
        with open('./google-key.json', 'r') as f:
            google_secret = json.load(f)

        client = service_account_from_dict(google_secret)


def get_client() -> Optional[Client]:
    global client

    if not client:
        init_client()

    return client
