from typing import Literal
from odetam import DetaModel


class User(DetaModel):
    access_key: str
    name: str
    mode: Literal['superuser', 'admin', 'employee']
