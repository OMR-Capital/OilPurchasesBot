from os import getenv

from gspread.worksheet import Worksheet

from google_sheets_utils.worksheet import get_worksheet, update_header
from sheet_data_utils.purchases import PURCHASES_HEADER

raw_worksheet = None
sorted_worksheet = None


def init_purchases_raw_worksheet() -> Worksheet:
    global raw_worksheet

    if not raw_worksheet:
        raw_worksheet = get_worksheet(
            getenv('TABLE_NAME', ''),
            getenv('STATS_PURCHASES_RAW_WORKSHEET', '')
        )

    if not raw_worksheet:
        raise Exception('Worksheet creation failed.')

    update_header(raw_worksheet, PURCHASES_HEADER)
    return raw_worksheet


def init_purchases_sorted_worksheet() -> Worksheet:
    global sorted_worksheet

    if not sorted_worksheet:
        sorted_worksheet = get_worksheet(
            getenv('TABLE_NAME', ''),
            getenv('STATS_PURCHASES_SORTED_WORKSHEET', '')
        )

    if not sorted_worksheet:
        raise Exception('Worksheet creation failed.')

    update_header(sorted_worksheet, PURCHASES_HEADER)
    return sorted_worksheet
