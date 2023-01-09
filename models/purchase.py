from datetime import datetime
from odetam import DetaModel


class Purchase(DetaModel):
    supplier: str
    amount: str
    price: str
    card: str
    approved: bool
    approved_by: str
    approve_date: datetime
    created_by: str
    create_date: datetime
