from datetime import datetime, timedelta, timezone


MSC_TZ = timezone(timedelta(hours=3), name='Europe/Moscow')


RU_MONTHS = [
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
]

RU_WEEKDAYS = [
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',
]


def datetime_to_str(date: datetime) -> str:
    return date.astimezone(MSC_TZ).strftime('%d.%m.%Y %H:%M')


def get_month_name(month: int) -> str:
    return RU_MONTHS[month - 1]


def get_weekday_name(weekday: int) -> str:
    return RU_WEEKDAYS[weekday]
