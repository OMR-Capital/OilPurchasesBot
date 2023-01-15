START = 'Я помогу Вам управлять закупками!'

ASK_ACCESS_KEY = 'Введите ключ доступа:'
ASK_NAME = 'Укажите ФИО:'
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
ASK_AMOUNT = 'Укажите объем вывезенного масла в литрах:'
ASK_PRICE = 'Укажите цену за литр:'
ASK_CARD = 'Укажите реквизиты для оплаты:'


PURCHASE_BASE=''' 
Тип договора: {contract_type}
Клиент: {client_type}
Поставщик: {supplier}
Объем (литров): {amount}
Цена (за литр): {price}
Реквизиты для оплаты: 
<code>{card}</code>
'''

PURCHASE_NOTIFICATION = '''
Отправитель: {creator}
Время: {time}

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

ERROR = 'Произошла какая-то ошибка. Попробуйте снова.'

TEST='TEST'