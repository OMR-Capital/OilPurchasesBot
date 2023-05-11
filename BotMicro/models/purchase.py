from datetime import datetime
from typing import Optional
from odetam import DetaModel


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

