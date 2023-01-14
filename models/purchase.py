from datetime import datetime
from typing import Optional
from odetam import DetaModel


class Purchase(DetaModel):
    contract_type: str
    supplier: str
    amount: str
    price: str
    card: str
    approved: bool
    approver: Optional[str]
    approve_time: Optional[datetime]
    creator: str
    create_time: datetime

    class Config:
        table_name = 'purchases'
        
