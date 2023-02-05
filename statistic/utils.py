from datetime import datetime

from utils.constants import MSC_TZ


def get_formatted_time(dt: datetime) -> str:
    return dt.astimezone(MSC_TZ).strftime('%d.%m.%Y %H:%M')
