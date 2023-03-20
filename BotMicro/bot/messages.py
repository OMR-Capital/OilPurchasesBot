from typing import Literal


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
Имя: {name}
Статус: {mode}
Регион: {area}
Ключ: <code>{access_key}</code>
'''

SUCCESSFUL_CREATE_USER = '''
Новый аккаунт добавлен.
''' + USER_INFO

ACCOUNTS_LIST = 'Нажмите на пользователя, чтобы посмотреть данные и статистику или удалить.'
SUCCESSFUL_DELETE_USER = 'Пользователь успешно удален.'

ASK_SUPPLIER = 'Укажите наименование поставщика:'
ASK_CONTRACT_TYPE = 'Выберите тип договора:'
ASK_CLIENT_TYPE = 'Выберите принадлежность клиента:'
ASK_UNIT = 'Выберете единицу измерения:'
ASK_INN = 'Укажите ИНН клиента:'

def ask_amount(unit: Literal['liter', 'kg']) -> str:
    unit_name = 'литрах' if unit == 'liter' else 'килограммах'
    return f'Укажите объем вывезенного масла в {unit_name}:'

def ask_price(unit: Literal['liter', 'kg']) -> str:
    unit_name = 'литр' if unit == 'liter' else 'килограмм'
    return f'Укажите цену за {unit_name}:'

ASK_CARD = 'Укажите реквизиты для оплаты:'
ASK_BANK = 'Укажите наименование банка оплаты:'
WRONG_INTEGER = 'Значение должно быть числом.\nПопробуйте снова:'


PURCHASE_BASE=''' 
Тип договора: {contract_type}
Клиент: {client_type}
Поставщик: {supplier}
Объем (литров): {amount:.3f}
Цена (за литр): {price:.3f}
ИНН: 
<code>{inn}</code>
Реквизиты для оплаты: 
<code>{card}</code>
Банк: {bank}
'''

PURCHASE_NOTIFICATION = '''
Отправитель: {creator}
Время: {time}

Полная стоимость: {full_price:.3f}
''' + PURCHASE_BASE

SUCCESSFUL_CREATE_PURCHASE = '''
Запись успешно создана и отправлена администраторам.
Вы получите сообщение, как только они ее подтвердят.

''' + PURCHASE_BASE

PURCHASE_APPROVED = '''
Заявка подтверждена.
Администратор: {approver}

''' + PURCHASE_BASE

SUCCESSFUL_MAKE_STATISTIC = 'Отчет успешно создан.'

ASK_FUELING_COST = 'Укажите стоимость заправки:' 
SUCCESSFUL_CREATE_FUELING = 'Запись о заправке успешно добавлена.'

ERROR = 'Произошла какая-то ошибка. Попробуйте снова.' 

TEST='TEST'