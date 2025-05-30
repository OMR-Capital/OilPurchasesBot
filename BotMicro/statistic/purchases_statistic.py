from os import getenv
from typing import Any

from models import Purchase, User
from statistic.google_sheets import get_sheet, get_worksheet, update_worksheet
from statistic.types import TableData, TableFormats
from statistic.utils import get_cell_literal, get_formatted_time, get_rows_range


TABLE_HEAD = [
    'Период',
    'Объем',
    'Стоимость',
    'Тип договора',
    'Клиент',
    'Время создания',
    'Создатель заявки',
    'Поставщик',
    'Объем (в литрах)',
    'Цена (за литр)',
    'Счет оплаты',
    'Регион',
    'Время одобрения',
    'Одобривший заявку',
    'Ключ'
]
TITLE_FORMAT = {
    'textFormat': {'bold': True, 'fontSize': 10},
    'horizontalAlignment': 'LEFT'
}
DAY_STATS_FORMAT = {
    'backgroundColor': {'red': 0.8, 'green': 0.66, 'blue': 0.66},
    'textFormat': {'bold': True, 'fontSize': 10},
    'horizontalAlignment': 'LEFT'
}
WEEK_STATS_FORMAT = {
    'backgroundColor': {'red': 0.66, 'green': 0.8, 'blue': 0.66},
    'textFormat': {'bold': True, 'fontSize': 10},
    'horizontalAlignment': 'LEFT'
}
MONTH_STATS_FORMAT = {
    'backgroundColor': {'red': 0.66, 'green': 0.66, 'blue': 0.8},
    'textFormat': {'bold': True, 'fontSize': 10},
    'horizontalAlignment': 'LEFT'
}


def get_purchase_statistic_row(purchase: Purchase, users: dict[str, User]) -> list[Any]:
    creator = users.get(purchase.creator)
    creator_name = creator.name if creator else ''

    approver = users.get(purchase.approver) if purchase.approver else None
    approver_name = approver.name if approver else ''

    create_time = get_formatted_time(purchase.create_time)

    if purchase.approve_time:
        approve_time = get_formatted_time(purchase.approve_time)
    else:
        approve_time = ''

    if purchase.card:
        purchase.card = "'" + purchase.card

    return [
        '', '', '',
        purchase.contract_type,
        purchase.client_type,
        create_time,
        creator_name,
        purchase.supplier,
        purchase.amount,
        purchase.price,
        purchase.card,
        purchase.area or '',
        approve_time,
        approver_name,
        purchase.key
    ]


def get_day_statistic_row(purchases: list[Purchase]) -> list[Any]:
    if not purchases:
        return []

    total_amount = sum(purchase.amount for purchase in purchases)
    total_price = sum(purchase.amount *
                      purchase.price for purchase in purchases)
    date = purchases[-1].create_time.strftime('%A %d.%m.%Y')
    return [f'{date}'.upper(), total_amount, total_price]


def get_week_statistic_row(purchases: list[Purchase]) -> list[Any]:
    if not purchases:
        return []

    total_amount = sum(purchase.amount for purchase in purchases)
    total_price = sum(purchase.amount *
                      purchase.price for purchase in purchases)
    begin_date = purchases[-1].create_time.strftime('%d.%m.%Y')
    end_date = purchases[0].create_time.strftime('%d.%m.%Y')
    return [f'неделя {begin_date} - {end_date}'.upper(), total_amount, total_price]


def get_month_statistic_row(purchases: list[Purchase]) -> list[Any]:
    if not purchases:
        return []

    total_amount = sum(purchase.amount for purchase in purchases)
    total_price = sum(purchase.amount *
                      purchase.price for purchase in purchases)
    begin_date = purchases[-1].create_time.strftime('%B %d.%m.%Y')
    end_date = purchases[0].create_time.strftime('%d.%m.%Y')
    return [f'{begin_date} - {end_date}'.upper(), total_amount, total_price]


def get_purchases_statistic(purchases: list[Purchase], users: dict[str, User]) -> tuple[TableData, TableFormats]:
    purchases.sort(key=lambda purchase: purchase.create_time)

    day_purchases: list[Purchase] = []
    day_rows: list[int] = []
    week_purchases: list[Purchase] = []
    week_rows: list[int] = []
    month_purchases: list[Purchase] = []
    month_rows: list[int] = []

    table_data: list[list[str]] = []
    for i in range(len(purchases)):
        purchase = purchases[i]
        next_purchase = purchases[i + 1] if i + 1 < len(purchases) else None

        table_data.append(get_purchase_statistic_row(purchase, users))
        day_purchases.append(purchase)
        week_purchases.append(purchase)
        month_purchases.append(purchase)

        if not next_purchase or purchase.create_time.date() != next_purchase.create_time.date():
            table_data.append(get_day_statistic_row(day_purchases))
            day_rows.append(len(table_data))
            day_purchases = []

        if not next_purchase or purchase.create_time.weekday() > next_purchase.create_time.weekday():
            table_data.append(get_week_statistic_row(week_purchases))
            week_rows.append(len(table_data))
            week_purchases = []

        if not next_purchase or purchase.create_time.month != next_purchase.create_time.month:
            table_data.append(get_month_statistic_row(month_purchases))
            month_rows.append(len(table_data))
            month_purchases = []

    day_rows = [len(table_data) - row + 1 for row in day_rows]
    week_rows = [len(table_data) - row + 1 for row in week_rows]
    month_rows = [len(table_data) - row + 1 for row in month_rows]

    table_data.append(TABLE_HEAD)
    table_data.reverse()

    title_formats = [
        {'range': get_rows_range([0], len(TABLE_HEAD))[
            0], 'format': TITLE_FORMAT}
    ]
    day_stats_formats = [
        {'range': row_range, 'format': DAY_STATS_FORMAT}
        for row_range in get_rows_range(day_rows, len(TABLE_HEAD))
    ]
    week_stats_formats = [
        {'range': row_range, 'format': WEEK_STATS_FORMAT}
        for row_range in get_rows_range(week_rows, len(TABLE_HEAD))
    ]
    month_stats_formats = [
        {'range': row_range, 'format': MONTH_STATS_FORMAT}
        for row_range in get_rows_range(month_rows, len(TABLE_HEAD))
    ]

    formats = title_formats + day_stats_formats + \
        week_stats_formats + month_stats_formats
    return table_data, formats


def update_purchases_statistic() -> None:
    users = {
        user.key: user
        for user in User.get_all() if user.key
    }

    sheet_name = getenv('GOOGLE_SHEET_NAME')
    if not sheet_name:
        raise Exception('GOOGLE_SHEET_NAME not specified')

    sheet = get_sheet(sheet_name)
    if not sheet:
        raise Exception('Cannot get sheet')

    purchases = Purchase.get_all()

    # full statistic
    purchases_worksheet = get_worksheet(sheet, 'Закупки')
    if not purchases_worksheet:
        raise Exception('Cannot get worksheet')

    stats_range = get_cell_literal(0, 0) + ':' + get_cell_literal(1000, len(TABLE_HEAD))

    table_data, formats = get_purchases_statistic(purchases, users)
    update_worksheet(purchases_worksheet, table_data, formats, [stats_range])
    # for each user
    for creator_key in set(purchase.creator for purchase in purchases):
        creator_name = users[creator_key].name
        user_purchases = [purchase for purchase in purchases if purchase.creator == creator_key]

        user_purchases_worksheet = get_worksheet(sheet, creator_name)
        if not user_purchases_worksheet:
            return None

        table_data, formats = get_purchases_statistic(user_purchases, users)
        update_worksheet(user_purchases_worksheet, table_data, formats, [stats_range])
