import json
from os import getenv
from typing import Optional

import gspread
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


def update_statistic_table(data: list[list[str]], table_name: str, worksheet_name: str):
    if service is None:
        init_service()

    try:
        sheet = service.open(table_name)
        worksheet = sheet.worksheet(worksheet_name)
        worksheet.clear()
        worksheet.update('A1', data)
    except:
        pass
