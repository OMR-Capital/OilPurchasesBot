from typing import Literal, Optional
from odetam import DetaModel


class User(DetaModel):
    access_key: str
    mode: Literal['superuser', 'admin', 'employee']
    name: str
    chat_id: Optional[int]
