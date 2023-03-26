from datetime import datetime
from typing import Optional
from odetam.async_model import AsyncDetaModel
from pydantic import Field


class PurchaseStats(AsyncDetaModel):
    """Statistic data of one purchase.
    Instead of model in backend (bot) all data like users' names are prefetched and stored as verbose strings
    """
    purchase_key: str = Field(..., alias='key')
    area: str
    contract_type: str
    client_type: str
    supplier: str
    inn: str
    amount: float
    price: float
    card: str
    bank: str
    creator: str
    create_time: datetime
    approved: bool
    approver: Optional[str]
    approve_time: Optional[datetime]
