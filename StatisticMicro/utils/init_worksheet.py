from os import getenv
from gspread.worksheet import Worksheet

from google_sheets_utils.worksheet import get_worksheet, update_header_row
from sheet_data_utils.applications import build_applications_header


worksheet = None


def init_applications_worksheet() -> Worksheet:
    global worksheet

    if not worksheet:
        worksheet = get_worksheet(getenv('TABLE_NAME', ''), getenv('WORKSHEET_NAME', ''))
        
    if not worksheet:
        raise Exception('Worksheet creation failed.')

    if worksheet.row_count == 1:  # type: ignore
        header_row = build_applications_header()
        update_header_row(worksheet, header_row)

    return worksheet
