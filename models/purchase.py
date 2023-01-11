from datetime import datetime
from odetam import DetaModel


class Purchase(DetaModel):
    supplier: str
    amount: str
    price: str
    card: str
    approved: bool
    approver_key: str
    approve_date: datetime
    creator_key: str
    create_date: datetime
