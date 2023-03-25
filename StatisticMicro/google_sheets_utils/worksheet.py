from typing import Any, Optional

from gspread.exceptions import WorksheetNotFound
from gspread.spreadsheet import Spreadsheet
from gspread.utils import ValueInputOption
from gspread.worksheet import Worksheet

from google_sheets_utils.client import get_client


def get_worksheet(table_name: str, worksheet_name: str) -> Optional[Worksheet]:
    client = get_client()
    if not client:
        return None

    sheet: Spreadsheet = client.open(table_name)
    try:
        worksheet: Worksheet = sheet.worksheet(worksheet_name)
    except WorksheetNotFound:
        worksheet: Worksheet = sheet.add_worksheet(worksheet_name, rows=1, cols=1)

    return worksheet


def update_header_row(worksheet: Worksheet, header_data: list[Any]):
    worksheet.update(
        f'A1:L1',
        [header_data],
        value_input_option=ValueInputOption.user_entered
    )


def add_application_row(worksheet: Worksheet, row_data: list[Any]) -> int:
    worksheet.append_row(row_data, value_input_option=ValueInputOption.user_entered)
    worksheet.sort((10, 'des'), range='A2:L9999')
    return worksheet.row_count + 1


def update_application_row(worksheet: Worksheet, app_key: str, row_data: list[Any]):
    cell = worksheet.find(app_key, in_column=1, case_sensitive=True)
    worksheet.update(
        f'A{cell.row}:L{cell.row}',
        [row_data],
        value_input_option=ValueInputOption.user_entered
    )


def clear_application_row(worksheet: Worksheet, app_key: str):
    cell = worksheet.find(app_key, in_column=1, case_sensitive=True)
    worksheet.update(
        f'A{cell.row}:L{cell.row}',
        [[''] * 12],
        value_input_option=ValueInputOption.user_entered
    )
    worksheet.sort((10, 'des'), range='A2:L9999')
