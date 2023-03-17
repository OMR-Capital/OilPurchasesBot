import json
from os import getenv
from typing import Optional

import gspread
from gspread.worksheet import Worksheet
from gspread.spreadsheet import Spreadsheet
from gspread.exceptions import WorksheetNotFound
from deta import Drive
from gspread import Client

from statistic.types import TableData, TableFormats


EMPTY_FORMAT = {
    'backgroundColor': {'red': 1, 'green': 1, 'blue': 1},
    'textFormat': {'bold': False, 'fontSize': 10},
    'borders': {},
    'horizontalAlignment': 'RIGHT',
}


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


def get_sheet(sheet_name: str) -> Optional[Spreadsheet]:
    if service is None:
        init_service()

    try:
        return service.open(sheet_name)
    except Exception:
        return None


def get_worksheet(sheet: Spreadsheet, worksheet_name: str) -> Optional[Worksheet]:
    try:
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(worksheet_name, rows=1, cols=1)

        return worksheet
    except Exception:
        return None


def update_worksheet(worksheet: Worksheet, table_data: TableData, formats: TableFormats) -> None:
    worksheet.clear()
    worksheet.format('A1:Z10000', EMPTY_FORMAT)
    worksheet.update(table_data)
    worksheet.batch_format(formats)
