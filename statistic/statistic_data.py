from datetime import timedelta, timezone, datetime
from typing import Any

from models import Fueling, Purchase, User
from odetam.exceptions import ItemNotFound

TIMEZONE = timezone(timedelta(hours=3), name='Europe/Moscow')

PURCHASES_TABLE_HEAD = [
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
    'Одобривший заявку'
]


def format_datetime(dt: datetime) -> str:
    return dt.strftime('%d.%m.%Y %H:%M')


def make_purchases_statistic() -> list[list[Any]]:
    purchases = Purchase.get_all()
    purchases.sort(key=lambda purchase: purchase.create_time, reverse=True)

    statistic_data: list[list[Any]] = [PURCHASES_TABLE_HEAD]
    for purchase in purchases:
        try:
            creator = User.get(purchase.creator)
            creator_name = creator.name
        except ItemNotFound:
            creator_name = 'Error'

        if purchase.approver:
            try:
                approver = User.get(purchase.approver)
                approver_name = approver.name
            except ItemNotFound:
                approver_name = 'Error'
        else:
            approver_name = ''

        create_time = format_datetime(purchase.create_time.astimezone(TIMEZONE))

        if purchase.approve_time:
            approve_time = format_datetime(purchase.approve_time.astimezone(TIMEZONE))
        else:
            approve_time = ''

        statistic_data.append([
            purchase.key or '',
            purchase.contract_type,
            purchase.client_type,
            create_time,
            creator_name,
            purchase.supplier,
            purchase.amount,
            purchase.price,
            "'" + purchase.inn,
            "'" + purchase.card,
            approve_time,
            approver_name,
        ])

    return statistic_data


FUELING_TABLE_HEAD = [
    'Номер',
    'Работник',
    'Время',
    'Стоимость'
]


def make_fueling_statistic() -> list[list[Any]]:
    feelings = Fueling.get_all()
    feelings.sort(key=lambda fueling: fueling.time, reverse=True)

    statistic_data: list[list[Any]] = [FUELING_TABLE_HEAD]
    for fueling in feelings:
        try:
            employee = User.get(fueling.employee)
            employee_name = employee.name
        except ItemNotFound:
            employee_name = 'Error'

        time = format_datetime(fueling.time.astimezone(TIMEZONE))

        statistic_data.append([
            fueling.key or '',
            employee_name,
            time,
            fueling.cost,
        ])

    return statistic_data

