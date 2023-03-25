from models.application import Application
from utils.datetime import datetime_to_str


def build_applications_header() -> list[str]:
    return [
        'ID',
        'Статус',
        'Описание',
        'Фото',
        'Группа источников',
        'Источник',
        'Группа ошибок',
        'Ошибка',
        'Создатель',
        'Время создания',
        'Подтверждающий',
        'Время подтверждения'
    ]


def build_application_row(application: Application) -> list[str]:
    attribute = application.attributes.popitem() if application.attributes else None
    return [
        application.key,
        application.status,
        application.caption,
        '\n'.join(application.photos),
        application.guilty_category or '',
        application.guilty or '',
        attribute[0] if attribute else '',
        attribute[1] if attribute else '',
        application.creator,
        datetime_to_str(application.created_at),
        application.approver or '',
        datetime_to_str(application.approved_at) if application.approved_at else ''
    ]

