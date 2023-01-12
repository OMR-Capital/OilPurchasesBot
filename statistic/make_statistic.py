from models import Purchase, User
from odetam.exceptions import ItemNotFound


TABLE_HEAD = [
    'Номер',
    'Поставщик',
    'Объем',
    'Цена',
    'Счет оплаты',
    'Создатель заявки',
    'Время создания',
    'Одобривший заявку',
    'Время одобрения'
]


def make_statistic() -> list[list[str]]:
    purchases = Purchase.get_all()

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
            purchase.supplier,
            purchase.amount,
            purchase.price,
            purchase.card,
            creator_name,
            purchase.create_time.isoformat(' ', 'minutes'),
            approver_name,
            purchase.approve_time.isoformat(' ', 'minutes') if purchase.approve_time else ''
        ])
    
    return statistic_data