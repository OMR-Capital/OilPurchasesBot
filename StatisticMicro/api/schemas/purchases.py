from api.schemas.base import BaseRequest
from models.purchase import PurchaseStats


class PurchaseRequest(BaseRequest):
    purchase: PurchaseStats
