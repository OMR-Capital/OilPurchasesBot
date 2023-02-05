import json
from os import getenv
from typing import Optional

import gspread
from gspread import Worksheet
from gspread.exceptions import WorksheetNotFound
from deta import Drive
from gspread import Client

KEY_FILE = getenv('GOOGLE_KEY_FILE', '')

service: Optional[Client] = None


def load_key_file(file_path: str):
    drive = Drive('config')

    with open(file_path, 'r') as f:
        drive.put(KEY_FILE, f)


def init_service():
    global service

    drive = Drive('config')
    google_secret_file = drive.get(KEY_FILE)

    if not google_secret_file:
        return
    
    google_secret = json.loads(google_secret_file.read())
    service = gspread.service_account_from_dict(google_secret)


def get_worksheet(table_name: str, worksheet_name: str) -> Optional[Worksheet]:
    if service is None:
        init_service()

    try:
        sheet = service.open(table_name)
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(worksheet_name, rows=1, cols=1)
            
        return worksheet
    except Exception:
        return None
        