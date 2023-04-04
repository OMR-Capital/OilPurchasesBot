from os import getenv
from typing import Any

from gspread import Worksheet
from gspread.exceptions import APIError

from models import Fueling, User
from odetam.exceptions import ItemNotFound
from statistic.google_sheets import get_sheet, get_worksheet, update_worksheet
from statistic.types import TableData, TableFormats
from statistic.utils import get_formatted_time, get_rows_range


TABLE_HEAD = [
    'Номер',
    'Работник',
    'Время',
    'Стоимость'
]

TITLE_FORMAT = {
    'textFormat': {'bold': True, 'fontSize': 10},
    'horizontalAlignment': 'LEFT'
}


def get_fueling_row(fueling: Fueling) -> list[Any]:
    try:
        employee = User.get(fueling.employee) # type: ignore
        employee_name = employee.name
    except ItemNotFound:
        employee_name = 'Error'

    time = get_formatted_time(fueling.time)

    return [
        fueling.key or '',
        employee_name,
        time,
        fueling.cost,
    ]


def get_fuelings_statistic(worksheet: Worksheet, fuelings: list[Fueling]) -> tuple[TableData, TableFormats]:
    table_data: list[list[str]] = [TABLE_HEAD]
    for fueling in fuelings:
        table_data.append(get_fueling_row(fueling))

    formats: TableFormats = [
        {'range': get_rows_range([0], len(TABLE_HEAD)), 'format': TITLE_FORMAT}
    ]
    return table_data, formats


def update_fuelings_statistic() -> None:
    sheet_name = getenv('GOOGLE_SHEET_NAME')
    if not sheet_name:
        return

    sheet = get_sheet(sheet_name)
    if not sheet:
        return

    worksheet = get_worksheet(sheet, 'Заправки')
    if not worksheet:
        return

    fuelings = Fueling.get_all()
    fuelings.sort(key=lambda fueling: fueling.time, reverse=True)

    table_data, formats = get_fuelings_statistic(worksheet, fuelings)
    try:
        update_worksheet(worksheet, table_data, formats)
    except APIError:
        return
