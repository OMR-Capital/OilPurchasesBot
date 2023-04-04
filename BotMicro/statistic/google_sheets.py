import json
from typing import Optional

import gspread
from gspread import Client
from gspread.exceptions import WorksheetNotFound
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet

from statistic.types import TableData, TableFormats

EMPTY_FORMAT = {
    'backgroundColor': {'red': 1, 'green': 1, 'blue': 1},
    'textFormat': {'bold': False, 'fontSize': 10},
    'borders': {},
    'horizontalAlignment': 'RIGHT',
}
KEY_FILE = 'google-key.json'


service: Optional[Client] = None


def init_service():
    global service

    with open(KEY_FILE, 'r') as f:
        google_secret = json.load(f)

    service = gspread.service_account_from_dict(google_secret)


def get_sheet(sheet_name: str) -> Spreadsheet:
    if service is None:
        init_service()

    return service.open(sheet_name)


def get_worksheet(sheet: Spreadsheet, worksheet_name: str) -> Worksheet:
    try:
        worksheet = sheet.worksheet(worksheet_name)
    except WorksheetNotFound:
        worksheet = sheet.add_worksheet(worksheet_name, rows=1, cols=1)

    return worksheet


def update_worksheet(worksheet: Worksheet, table_data: TableData, formats: TableFormats) -> None:
    worksheet.clear()
    worksheet.format('A1:Z10000', EMPTY_FORMAT)
    worksheet.update(table_data)
    worksheet.batch_format(formats)
