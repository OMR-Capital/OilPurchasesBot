from datetime import datetime
from typing import Any

from gspread.worksheet import Worksheet

from utils.datetime import MSC_TZ


def get_formatted_time(dt: datetime) -> str:
    return dt.astimezone(MSC_TZ).strftime('%d.%m.%Y %H:%M')


def get_cell_literal(row: int, column: int) -> str:
    return f'{chr(65 + column)}{row + 1}'


def get_rows_range(rows_numbers: list[int], row_width: int) -> list[str]:
    return [
        f'{get_cell_literal(row, 0)}:{get_cell_literal(row, row_width - 1)}'
        for row in rows_numbers
    ]


def get_cols_range(cols_numbers: list[int], row_width: int) -> list[str]:
    return [
        f'{get_cell_literal(0, col)}:{get_cell_literal(row_width - 1, col)}'
        for col in cols_numbers
    ]