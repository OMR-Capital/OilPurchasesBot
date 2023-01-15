import json
from os import getenv
from typing import Optional

import gspread
from deta import Drive
from gspread import Client

KEY_FILE = getenv('GOOGLE_KEY_FILE', '')
SHEET_NAME = getenv('GOOGLE_SHEET_NAME')
WORKSHEET_NAME = getenv('GOOGLE_WORKSHEET_NAME')


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


def update_statistic_table(data: list[list[str]]):
    if service is None:
        init_service()

    try:
        sheet = service.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        worksheet.clear()
        worksheet.update('A1', data)
    except:
        pass
