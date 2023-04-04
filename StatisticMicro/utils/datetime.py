from datetime import datetime, timedelta, timezone


MSC_TZ = timezone(timedelta(hours=3), name='Europe/Moscow')


def datetime_to_str(date: datetime) -> str:
    return date.astimezone(MSC_TZ).strftime('%d.%m.%Y %H:%M')
