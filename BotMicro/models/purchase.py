from datetime import datetime
from enum import Enum
from typing import Optional
from odetam import DetaModel
from pydantic import validator

from utils.awesome_random import awesome_string


class ClientType(str, Enum):
    MANAGER = 'Менеджерский'
    OWN = 'Собственный'


class ContractType(str, Enum):
    CASH = 'Нал'
    CASHLESS = 'Безнал'


class Unit(str, Enum):
    KG = 'кг'
    LITERS = 'л'


class Purchase(DetaModel):
    area: Optional[str] = None
    contract_type: ContractType
    client_type: ClientType
    supplier: str
    inn: Optional[str] = None # deprecated
    amount: float
    price: float
    card: str
    bank: str
    approved: bool
    approver: Optional[str]
    approve_time: Optional[datetime]
    creator: str
    create_time: datetime

    class Config:
        table_name = 'purchases'

    @validator('key', pre=True, always=True)
    def set_key(cls, key: Optional[str]) -> str:
        return key or awesome_string(length=6)
