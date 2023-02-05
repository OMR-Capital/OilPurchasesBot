from os import getenv
from typing import Any

from gspread import Worksheet

from models import Fueling, User
from odetam.exceptions import ItemNotFound
from statistic.google_sheets import get_worksheet
from statistic.utils import get_formatted_time


TABLE_HEAD = [
    'Номер',
    'Работник',
    'Время',
    'Стоимость'
]


def get_fueling_row(fueling: Fueling) -> list[Any]:
    try:
        employee = User.get(fueling.employee)
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


def create_fuelings_statistic(table_name: str, worksheet_name: str, fuelings: list[Fueling]) -> None:
    worksheet = get_worksheet(table_name, worksheet_name)
    if not worksheet:
        return

    worksheet.clear()

    table_data: list[list[str]] = [TABLE_HEAD]
    for fueling in fuelings:
        table_data.append(get_fueling_row(fueling))

    worksheet.update('A1', table_data)
    format_fuelings_statistic(worksheet)


def format_fuelings_statistic(worksheet: Worksheet) -> None:
    worksheet.format('A1:D1', {
        'textFormat': {
            'bold': True
        }
    })


def update_fuelings_statistic() -> None:
    table_name = getenv('GOOGLE_SHEET_NAME')
    if not table_name:
        return

    fuelings = Fueling.get_all()
    fuelings.sort(key=lambda fueling: fueling.time, reverse=True)

    create_fuelings_statistic(
        table_name,
        'Заправки',
        fuelings
    )

