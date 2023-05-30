from fastapi import APIRouter, Depends, HTTPException, status
from gspread.worksheet import Worksheet

from api.schemas.base import BaseResponse, FailureResponse, SuccessResponse
from api.schemas.purchases import (PurchaseRequest, PurchaseResponse,
                                   PurchasesResponse)
from api.stubs import PurchasesRawWorksheetStub, PurchasesSortedWorksheetStub
from google_sheets_utils.worksheet import (add_row, remove_row_by_key,
                                           sort_by_column, update_row_by_key)
from models.purchase import PurchaseStats
from sheet_data_utils.purchases import CREATE_TIME_COLUMN, build_purchase_row

purchases_router = APIRouter(prefix='/purchase', tags=['Purchases'])


@purchases_router.get('/')
async def get_purchases() -> PurchasesResponse:
    purchases = await PurchaseStats.get_all()
    return PurchasesResponse(ok=True, purchases=purchases)


@purchases_router.get('/{purchase_key}')
async def get_purchase(
    purchase_key: str,
) -> PurchaseResponse:
    purchase = await PurchaseStats.get_or_none(purchase_key)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Purchase {purchase_key} not found.'
        )

    return PurchaseResponse(ok=True, purchase=purchase)


@purchases_router.post('/')
async def add_purchase(
    request: PurchaseRequest,
    raw_worksheet: Worksheet = Depends(PurchasesRawWorksheetStub),
    sorted_worksheet: Worksheet = Depends(PurchasesSortedWorksheetStub),
) -> BaseResponse:
    purchase_key = request.purchase.purchase_key
    old_purchase = await PurchaseStats.get_or_none(purchase_key)
    if old_purchase:
        return FailureResponse(
            detail=f'Purchase {old_purchase.key} already exists in statistic'
        )

    purchase_row = build_purchase_row(request.purchase)
    try:
        add_row(raw_worksheet, purchase_row)
        add_row(sorted_worksheet, purchase_row)
        sort_by_column(sorted_worksheet, CREATE_TIME_COLUMN, reverse=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Fail to append row to worksheet: {e}'
        )

    await request.purchase.save()
    return SuccessResponse(detail=str(raw_worksheet))


@purchases_router.patch('/{purchase_key}')
async def update_purchase(
    purchase_key: str,
    request: PurchaseRequest,
    raw_worksheet: Worksheet = Depends(PurchasesRawWorksheetStub),
    sorted_worksheet: Worksheet = Depends(PurchasesSortedWorksheetStub),
) -> BaseResponse:
    old_purchase = await PurchaseStats.get_or_none(purchase_key)
    if not old_purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Purchase {purchase_key} not found.'
        )

    purchase_row = build_purchase_row(request.purchase)
    try:
        update_row_by_key(raw_worksheet, purchase_key, purchase_row)
        update_row_by_key(sorted_worksheet, purchase_key, purchase_row)
        sort_by_column(sorted_worksheet, CREATE_TIME_COLUMN, reverse=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Fail to update row to worksheet: {e}'
        )

    await request.purchase.save()
    return SuccessResponse(detail=str(raw_worksheet))


@purchases_router.delete('/{purchase_key}')
async def remove_purchase(
    purchase_key: str,
    raw_worksheet: Worksheet = Depends(PurchasesRawWorksheetStub),
    sorted_worksheet: Worksheet = Depends(PurchasesSortedWorksheetStub),
) -> BaseResponse:
    purchase = await PurchaseStats.get_or_none(purchase_key)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Purchase {purchase_key} not found.'
        )

    try:
        remove_row_by_key(raw_worksheet, purchase_key)
        remove_row_by_key(sorted_worksheet, purchase_key)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Fail to update row at worksheet: {e}'
        )

    await purchase.delete()
    return SuccessResponse(detail=str(raw_worksheet))
