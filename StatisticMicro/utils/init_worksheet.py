from os import getenv

from gspread.worksheet import Worksheet

from google_sheets_utils.worksheet import get_worksheet, update_header
from sheet_data_utils.purchases import PURCHASES_HEADER

worksheet = None


def init_purchases_worksheet() -> Worksheet:
    global worksheet

    if not worksheet:
        worksheet = get_worksheet(getenv('TABLE_NAME', ''), getenv('PURCHASES_WORKSHEET_NAME', ''))
        
    if not worksheet:
        raise Exception('Worksheet creation failed.')

    update_header(worksheet, PURCHASES_HEADER)
    return worksheet
