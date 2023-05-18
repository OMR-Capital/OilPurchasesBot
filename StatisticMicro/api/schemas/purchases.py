from api.schemas.base import BaseRequest, BaseResponse
from models.purchase import PurchaseStats


class PurchaseRequest(BaseRequest):
    purchase: PurchaseStats


class PurchasesResponse(BaseResponse):
    purchases: list[PurchaseStats]


class PurchaseResponse(BaseResponse):
    purchase: PurchaseStats
