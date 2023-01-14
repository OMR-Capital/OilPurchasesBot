from models import Purchase, User
from odetam.exceptions import ItemNotFound


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

        statistic_data.append([
            purchase.key or '',
            purchase.contract_type,
            purchase.create_time.isoformat(' ', 'minutes'),
            creator_name,
            purchase.supplier,
            purchase.amount,
            purchase.price,
            purchase.card,
            purchase.approve_time.isoformat(' ', 'minutes') if purchase.approve_time else '',
            approver_name,
        ])
    
    return statistic_data