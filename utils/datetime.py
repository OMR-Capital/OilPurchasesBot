import locale
from datetime import timedelta, timezone


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

MSC_TZ = timezone(timedelta(hours=3), name='Europe/Moscow')

WEEKDAYS = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
]
