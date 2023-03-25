from datetime import datetime
from enum import Enum
from typing import Optional

from odetam.async_model import AsyncDetaModel
from pydantic import BaseConfig


class ApplicationStatus(str, Enum):
    approved = 'Подтверждена'
    new = 'Ждет обработки'


class Application(AsyncDetaModel):
    status: ApplicationStatus

    caption: str
    photos: list[str]  # links to photos

    creator: str
    created_at: datetime

    guilty_category: Optional[str]
    guilty: Optional[str]
    attributes: Optional[dict[str, str]]

    approver: Optional[str]
    approved_at: Optional[datetime] = None

    editor: Optional[str] = None
    last_edited_at: Optional[datetime] = None

    class Config(BaseConfig):
        table_name = 'analytics_applications'
