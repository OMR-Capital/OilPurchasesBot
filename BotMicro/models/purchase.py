from datetime import datetime
from typing import Optional
from odetam import DetaModel
from pydantic import validator

from utils.awesome_random import awesome_string


class Purchase(DetaModel):
    area: Optional[str] = None
    contract_type: str
    client_type: str
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
