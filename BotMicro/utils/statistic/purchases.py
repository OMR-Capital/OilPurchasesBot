from typing import Any, Optional

from pydantic import BaseModel

from models.purchase import Purchase
from models.user import User
from utils.micro_api.requests import request_micro


class PurchaseData(BaseModel):
    """Purchase representation for request to StatisticMicro"""

    key: str
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
    create_time: str
    approved: bool
    approver: Optional[str]
    approve_time: Optional[str]


async def get_statistic_data(purchase: Purchase) -> Optional[dict[str, dict[str, Any]]]:
    if purchase.key is None:
        return None

    creator = User.get_or_none(purchase.creator)
    if creator is None:
        return None

    if purchase.approver:
        approver = User.get_or_none(purchase.approver)
        if approver is None:
            return None
    else:
        approver = None

    purchase_stat = PurchaseData(
        key=purchase.key,
        area=purchase.area or '',
        contract_type=purchase.contract_type,
        client_type=purchase.client_type,
        supplier=purchase.supplier,
        inn=purchase.inn,
        amount=purchase.amount,
        price=purchase.price,
        card=purchase.card,
        bank=purchase.bank,
        creator=creator.name,
        create_time=purchase.create_time.isoformat(),
        approved=purchase.approved,
        approver=approver.name if approver else None,
        approve_time=purchase.approve_time.isoformat() if purchase.approve_time else None,
    )

    data = {'purchase': purchase_stat.dict()}
    return data


async def add_purchase_stats(purchase: Purchase) -> Optional[dict[str, Any]]:
    data = await get_statistic_data(purchase)
    if data is None:
        raise Exception('Purchase data is None')

    result = await request_micro(
        method='POST',
        micro='statistic',
        route='/purchase',
        data=data
    )

    return result


async def update_purchase_stats(purchase: Purchase) -> Optional[dict[str, Any]]:
    data = await get_statistic_data(purchase)
    if data is None:
        raise Exception('Purchase data is None')

    result = await request_micro(
        method='PATCH',
        micro='statistic',
        route=f'/purchase/{purchase.key}',
        data=data
    )

    return result
