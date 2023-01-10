from typing import Literal
from odetam import DetaModel


class User(DetaModel):
    access_key: str
    mode: Literal['superuser', 'admin', 'employee']
    name: str
    chat_id: int
