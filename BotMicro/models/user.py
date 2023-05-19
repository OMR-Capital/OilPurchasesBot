from enum import Enum
from random import choices, choice
from string import ascii_lowercase, digits
from typing import Optional

from odetam import DetaModel


class UserMode(str, Enum):
    SUPERUSER = 'superuser'
    ADMIN = 'admin'
    EMPLOYEE = 'employee'

    @classmethod
    def get_name(cls, mode: 'UserMode') -> str:
        if mode == cls.SUPERUSER:
            return 'Владелец'
        elif mode == cls.ADMIN:
            return 'Администратор'
        elif mode == cls.EMPLOYEE:
            return 'Сотрудник'
        else:
            return 'Неизвестный режим'


class User(DetaModel):
    access_key: str
    name: str
    mode: UserMode
    area: Optional[str] = None
    chat_id: Optional[int]

    class Config:
        table_name = 'users'

    @classmethod
    def register_user(cls, name: str, area: str, mode: UserMode) -> 'User':
        access_key = choice(digits) + ''.join(choices(ascii_lowercase + digits, k=6))

        user = User(
            access_key=access_key,
            name=name,
            mode=mode,
            area=area
        )
        user.save()
        return user

    @classmethod
    def login_user(cls, access_key: str, chat_id: int) -> Optional['User']:
        result = User.query(User.access_key == access_key) # type: ignore

        if result:
            user = result.pop()
            user.chat_id = chat_id
            user.save()
            return user

        return None
