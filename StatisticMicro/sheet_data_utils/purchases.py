from typing import Any
from models.purchase import PurchaseStats
from utils.datetime import datetime_to_str, get_month_name, get_weekday_name


CREATE_TIME_COLUMN = 4 # for sorting in GoogleSheets

PURCHASES_HEADER = [
    'ID',
    'Тип договора',
    'Клиент',
    'Время создания',
    'Создатель заявки',
    'Поставщик',
    'Объем (в литрах)',
    'Цена (за литр)',
    'ИНН',
    'Счет оплаты',
    'Регион',
    'Время одобрения',
    'Одобривший заявку',
    'День',
    'Неделя',
    'Месяц',
]


def build_purchase_row(purchase: PurchaseStats) -> list[Any]:
    return [
        purchase.key or '',
        purchase.contract_type,
        purchase.client_type,
        datetime_to_str(purchase.create_time),
        purchase.creator,
        purchase.supplier,
        purchase.amount,
        purchase.price,
        purchase.inn or '',
        "'" + purchase.card,
        purchase.area,
        datetime_to_str(purchase.approve_time) if purchase.approve_time else '',
        purchase.approver or '',
        str(purchase.create_time.day),
        get_weekday_name(purchase.create_time.weekday()),
        get_month_name(purchase.create_time.month),
    ]
