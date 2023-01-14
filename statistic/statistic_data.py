from datetime import timedelta, timezone

from models import Purchase, User
from odetam.exceptions import ItemNotFound


TIMEZONE = timezone(timedelta(hours=3), name='Europe/Moscow')

TABLE_HEAD = [
    'Номер',
    'Тип договора',
    'Время создания',
    'Создатель заявки',
    'Поставщик',
    'Объем (в литрах)',
    'Цена (за литр)',
    'Счет оплаты',
    'Время одобрения'
    'Одобривший заявку',
]


def make_statistic() -> list[list[str]]:
    purchases = Purchase.get_all()
    purchases.sort(key=lambda purchase: purchase.create_time, reverse=True)

    statistic_data = [TABLE_HEAD]
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

        create_time = purchase.create_time.astimezone(TIMEZONE).isoformat(' ', 'minutes')

        if purchase.approve_time:
            approve_time = purchase.approve_time.astimezone(TIMEZONE).isoformat(' ', 'minutes')  
        else:
            approve_time = ''
            
        statistic_data.append([
            purchase.key or '',
            purchase.contract_type,
            create_time,
            creator_name,
            purchase.supplier,
            purchase.amount,
            purchase.price,
            purchase.card,
            approve_time,
            approver_name,
        ])

    return statistic_data
