from models.purchase import Purchase, Unit

START = 'Я помогу Вам управлять закупками!'

ASK_ACCESS_KEY = 'Введите ключ доступа:'
ASK_NAME = 'Укажите ФИО:'
ASK_AREA = 'Укажите регион:'
WRONG_ACCESS_KEY = 'Неверный ключ.\nПопробуйте ввести снова.'

SUCCESSFUL_SUPERUSER_LOGIN = 'Здравствуйте, {name}! Вы успешно вошли в кабинет руководителя.\nВы сможете управлять закупками и аккаунтами других пользователей.'
SUCCESSFUL_ADMIN_LOGIN = 'Здравствуйте, {name}! Вы успешно вошли в кабинет администратора.\nСюда будут приходить уведомления о новых закупках.'
SUCCESSFUL_EMPLOYEE_LOGIN = 'Здравствуйте, {name}! Вы успешно вошли в кабинет работника.'

LOAD_PAGE = 'Загрузка меню'
WAIT = 'Идет обработка...'
MAIN_PAGE = 'Основное меню'

ACCOUNTS = 'Управление аккаунтами'

USER_INFO = '''
<b>Имя</b>: {name}
<b>Статус</b>: {mode}
<b>Регион</b>: {area}
Ключ: <code>{access_key}</code>
'''

SUCCESSFUL_CREATE_USER = '''
Новый аккаунт добавлен.
''' + USER_INFO

ACCOUNTS_LIST = 'Нажмите на пользователя, чтобы посмотреть данные и статистику или удалить.'
SUCCESSFUL_DELETE_USER = 'Пользователь успешно удален.'

ACQUIRERS = 'Управление покупателями'
ACQUIRERS_LIST = 'Покупатели (нажмите на кнопку покупателя, чтобы удалить его):'
ASK_ACQUIRER_NAME = 'Укажите наименование покупателя:'
ASK_CONFIRM_DELETE_ACQUIRER = 'Вы уверены, что хотите удалить покупателя ?'
SUCCESSFUL_CREATE_ACQUIRER = 'Новый покупатель добавлен: {name}'
SUCCESSFUL_DELETE_ACQUIRER = 'Покупатель успешно удален.'

ASK_EDIT_PURCHASE_KEY = 'Введите ключ заявки:'
PURCHASE_NOT_FOUND = 'Заявка не найдена.'
SUCCESSFUL_EDIT_PURCHASE = 'Заявка успешно изменена.'

ASK_SUPPLIER = 'Укажите наименование поставщика:'
ASK_CONTRACT_TYPE = 'Выберите тип договора:'
ASK_CLIENT_TYPE = 'Выберите принадлежность клиента:'
ASK_UNIT = 'Выберете единицу измерения:'
ASK_INN = 'Укажите ИНН клиента:'


def ask_amount(unit: Unit) -> str:
    unit_name = 'литрах' if unit == Unit.LITERS else 'килограммах'
    return f'Укажите объем вывезенного масла в {unit_name}:'


def ask_price(unit: Unit) -> str:
    unit_name = 'литр' if unit == Unit.LITERS else 'килограмм'
    return f'Укажите цену за {unit_name}:'


ASK_CARD = 'Укажите реквизиты для оплаты:'
ASK_BANK = 'Укажите наименование банка оплаты:'
WRONG_INTEGER = 'Значение должно быть числом.\nПопробуйте снова:'


PURCHASE_BASE = '''
<b>Тип договора</b>: {contract_type}
<b>Клиент</b>: {client_type}
<b>Поставщик</b>: {supplier}
<b>Объем (литров)</b>: {amount:.3f}
<b>Цена (за литр)</b>: {price:.3f}
<b>Реквизиты для оплаты</b>:
<code>{card}</code>
<b>Банк</b>: {bank}
'''

PURCHASE_NOTIFICATION = '''
<b>Отправитель</b>: {creator}
<b>Время</b>: {time}

<b>Полная стоимость</b>: {full_price:.3f}
''' + PURCHASE_BASE

SUCCESSFUL_CREATE_PURCHASE = '''
Запись успешно создана и отправлена администраторам.
Вы получите сообщение, как только они ее подтвердят.

''' + PURCHASE_BASE

PURCHASE_APPROVED = '''
Заявка подтверждена.
<b>Администратор</b>: {approver}

''' + PURCHASE_BASE


def edit_purchase_ask(purchase: Purchase, question: str) -> str:
    purchase_info = PURCHASE_BASE.format(
        contract_type=purchase.contract_type,
        client_type=purchase.client_type,
        supplier=purchase.supplier,
        amount=purchase.amount,
        price=purchase.price,
        card=purchase.card,
        bank=purchase.bank
    )
    return f'{purchase_info}--------\n\n{question}'


SUCCESSFUL_MAKE_STATISTIC = 'Отчет успешно создан.'

ASK_FUELING_COST = 'Укажите стоимость заправки:'
SUCCESSFUL_CREATE_FUELING = 'Запись о заправке успешно добавлена.'

ERROR = 'Произошла какая-то ошибка. Попробуйте снова.'

TEST = 'TEST'


ASK_ACQUIRER = 'Выберите получателя:'

DISPATCH_BASE = '''
<b>Назначение</b>: {acquirer}
<b>Объем (литров)</b>: {amount:.3f}
'''

DISPATCH_NOTIFICATION = '''
<b>Отправитель</b>: {creator}
<b>Время</b>: {time}

<b>Регион</b>: {area}
''' + DISPATCH_BASE


SUCCESSFUL_CREATE_DISPATCH = '''
Отгрузка успешно создана.

''' + DISPATCH_BASE


def amount_statistics(
    total_purchased_amount: float,
    total_dispatched_amount: float,
    areas_amount: dict[str, float]
) -> str:
    return f'''
<b>Общий объем закупленного масла (литры)</b>: {total_purchased_amount:.3f}

<b>Общий объем отгруженного масла (килограммы)</b>: {total_dispatched_amount:.3f}

<b>Объем масла по регионам (литры)</b>:
''' + '\n'.join(f'{area}: {amount:.3f}' for area, amount in areas_amount.items())
