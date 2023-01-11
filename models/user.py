from random import choices, choice
from string import ascii_lowercase, digits
from typing import Literal, Optional

from odetam import DetaModel


class User(DetaModel):
    access_key: str
    name: str
    mode: str
    chat_id: Optional[int]

    class Config:
        table_name = 'users'

    @classmethod
    def register_user(cls, name: str, mode: Literal['superuser', 'admin', 'employee']) -> 'User':
        access_key = choice(digits) + ''.join(choices(ascii_lowercase + digits, k=6))

        user = User(
            access_key=access_key,
            name=name,
            mode=mode
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
