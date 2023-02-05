import locale
from os import getenv
from typing import Any

from gspread import Worksheet
from gspread.exceptions import APIError

from models import Purchase, User
from odetam.exceptions import ItemNotFound
from statistic.google_sheets import get_worksheet
from statistic.utils import get_formatted_time


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian" 
)

TABLE_HEAD = [
    'Номер',
    'Тип договора',
    'Клиент',
    'Время создания',
    'Создатель заявки',
    'Поставщик',
    'Объем (в литрах)',
    'Цена (за литр)',
    'ИНН',
    'Счет оплаты',
    'Время одобрения',
    'Одобривший заявку',
    'Итоги',
    'Объем',
    'Стоимость'
]


WEEKDAYS = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
]


def get_purchase_statistic_row(purchase: Purchase) -> list[Any]:
    try:
        creator = User.get(purchase.creator) # type: ignore
        creator_name = creator.name
    except ItemNotFound:
        creator_name = 'Error'

    if purchase.approver:
        try:
            approver = User.get(purchase.approver) # type: ignore
            approver_name = approver.name
        except ItemNotFound:
            approver_name = 'Error'
    else:
        approver_name = ''

    create_time = get_formatted_time(purchase.create_time)

    if purchase.approve_time:
        approve_time = get_formatted_time(purchase.approve_time)
    else:
        approve_time = ''

    if purchase.inn:
        purchase.inn = "'" + purchase.inn
    
    if purchase.card:
        purchase.card = "'" + purchase.card
    
    return [
        purchase.key or '',
        purchase.contract_type,
        purchase.client_type,
        create_time,
        creator_name,
        purchase.supplier,
        purchase.amount,
        purchase.price,
        purchase.inn,
        purchase.card,
        approve_time,
        approver_name,
    ]


def get_day_statistic_row(purchases: list[Purchase]) -> list[Any]:
    total_amount = sum(purchase.amount for purchase in purchases)
    total_price = sum(purchase.amount * purchase.price for purchase in purchases)
    date = purchases[-1].create_time.strftime('%A %d.%m.%Y')
    return [''] * len(TABLE_HEAD[:-3]) + [f'Итого за день {date}', total_amount, total_price]


def get_week_statistic_row(purchases: list[Purchase]) -> list[Any]:
    total_amount = sum(purchase.amount for purchase in purchases)
    total_price = sum(purchase.amount * purchase.price for purchase in purchases)
    begin_date = purchases[-1].create_time.strftime('%d.%m.%Y')
    end_date = purchases[0].create_time.strftime('%d.%m.%Y')
    return [''] * len(TABLE_HEAD[:-3]) + [f'Итого за неделю {begin_date} - {end_date}', total_amount, total_price]


def get_month_statistic_row(purchases: list[Purchase]) -> list[Any]:
    total_amount = sum(purchase.amount for purchase in purchases)
    total_price = sum(purchase.amount * purchase.price for purchase in purchases)
    begin_date = purchases[-1].create_time.strftime('%B %d.%m.%Y')
    end_date = purchases[0].create_time.strftime('%d.%m.%Y')
    return [''] * len(TABLE_HEAD[:-3]) + [f'Итого за месяц {begin_date} - {end_date}', total_amount, total_price]


def get_cell_literal(row: int, column: int) -> str:
    return f'{chr(65 + column)}{row + 1}'


def format_purchases_statistic(table_data: list[list[str]], statistic_rows: list[int], worksheet: Worksheet):    
    # clear formatting
    worksheet.format(
        'A1:Z1000', 
        {
            'borders': {}, 
            'textFormat': {}, 
            'backgroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}
        }
    )

    # set bottom line for statistic rows
    range_ = []
    for row in statistic_rows:
        begin = get_cell_literal(row, 0) 
        end = get_cell_literal(row, len(TABLE_HEAD) - 1) 
        range_.append(f'{begin}:{end}')

    worksheet.format(
        range_,
        {
            'borders': {
                'bottom': {
                    'style': 'SOLID', 
                    'width': 3, 
                    'color': {
                        'red': 0.0, 
                        'green': 0.0, 
                        'blue': 0.0
                    }
                }
            }
        }
    )

    # set bold for table head
    worksheet.format(
        f'A1:{get_cell_literal(0, len(TABLE_HEAD) - 2)}',
        {
            'textFormat': {
                'bold': True
            }
        }
    )

    # set right border between data and statistic
    begin = get_cell_literal(0, len(TABLE_HEAD) - 3)
    end = get_cell_literal(len(table_data), len(TABLE_HEAD) - 3)
    range_ = f'{begin}:{end}'
    worksheet.format(
        range_,
        {
            'borders': {
                'left': {
                    'style': 'SOLID',
                    'width': 3,
                    'color': {
                        'red': 0.0,
                        'green': 0.0,
                        'blue': 0.0
                    } 
                },
            }
        }
    )

    range_ = [
        get_cell_literal(row, len(TABLE_HEAD) - 3) 
        for row in statistic_rows
    ]
    worksheet.format(
        range_,
        {
            'borders': {
                'left': {
                    'style': 'SOLID',
                    'width': 3,
                    'color': {
                        'red': 0.0,
                        'green': 0.0,
                        'blue': 0.0
                    }   
                },
                'bottom': {
                    'style': 'SOLID',
                    'width': 3,
                    'color': {
                        'red': 0.0,
                        'green': 0.0,
                        'blue': 0.0
                    }   
                }
            }
        }
    )


def create_purchases_statistic(table_name: str, worksheet_name: str, purchases: list[Purchase]) -> None:
    worksheet = get_worksheet(table_name, worksheet_name)
    if not worksheet:
        return
    
    worksheet.clear()
    
    purchases.sort(key=lambda purchase: purchase.create_time, reverse=True)

    day_purchases: list[Purchase] = []
    week_purchases: list[Purchase] = []
    month_purchases: list[Purchase] = []
    statistic_rows: list[int] = []
    
    table_data: list[list[str]] = [TABLE_HEAD]
    for i in range(len(purchases)):
        purchase = purchases[i]
        table_data.append(get_purchase_statistic_row(purchase))

        day_purchases.append(purchase)
        week_purchases.append(purchase)
        month_purchases.append(purchase)
        
        next_purchase = purchases[i + 1] if i + 1 < len(purchases) else None
        if not next_purchase or purchase.create_time.day != next_purchase.create_time.day:
            table_data.append(get_day_statistic_row(day_purchases))
            statistic_rows.append(len(table_data) - 1)
            day_purchases.clear()

        if not next_purchase or purchase.create_time.weekday() < next_purchase.create_time.weekday():
            table_data.append(get_week_statistic_row(week_purchases))
            statistic_rows.append(len(table_data) - 1)
            week_purchases.clear()

        if not next_purchase or purchase.create_time.month != next_purchase.create_time.month:
            table_data.append(get_month_statistic_row(month_purchases))
            statistic_rows.append(len(table_data) - 1)
            month_purchases.clear()

    worksheet.update('A1', table_data, raw=False)
    format_purchases_statistic(table_data, statistic_rows, worksheet)


def update_purchases_statistic() -> None:
    table_name = getenv('GOOGLE_SHEET_NAME')
    if not table_name:
        return None
    
    purchases = Purchase.get_all()

    # full statistic
    try:
        create_purchases_statistic(table_name, 'Закупки', purchases)
    except APIError:
        return

    # for each user
    for user_key in set(purchase.creator for purchase in purchases):
        try:
            creator = User.get(user_key) # type: ignore
            creator_name = creator.name
        except ItemNotFound:
            creator_name = 'Error'
        
        user_purchases = [purchase for purchase in purchases if purchase.creator == user_key]
        try:
            create_purchases_statistic(table_name, creator_name, user_purchases)
        except APIError:
            return
    