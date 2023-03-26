from fastapi import APIRouter, Depends, HTTPException, status
from gspread.worksheet import Worksheet

from api.schemas.base import BaseResponse, FailureResponse, SuccessResponse
from api.schemas.purchases import PurchaseRequest
from api.stubs import PurchasesWorksheetStub
from google_sheets_utils.worksheet import (add_row, remove_row_by_key,
                                           sort_by_column, update_row_by_key)
from models.purchase import PurchaseStats
from sheet_data_utils.purchases import CREATE_TIME_COLUMN, build_purchase_row

purchases_router = APIRouter(prefix='/purchase', tags=['Purchases'])


@purchases_router.post('/')
async def add_purchase(
    request: PurchaseRequest,
    worksheet: Worksheet = Depends(PurchasesWorksheetStub)
) -> BaseResponse:
    old_purchase = await PurchaseStats.get_or_none(request.purchase.purchase_key)
    if old_purchase:
        return FailureResponse(detail=f'Purchase {old_purchase.key} already exists in statistic')

    purchase_row = build_purchase_row(request.purchase)
    try:
        add_row(worksheet, purchase_row)
        sort_by_column(worksheet, CREATE_TIME_COLUMN)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Fail to append row to worksheet: {e}'
        )

    await request.purchase.save()
    return SuccessResponse(detail=str(worksheet))


@purchases_router.patch('/{purchase_key}')
async def update_purchase(
    purchase_key: str,
    request: PurchaseRequest,
    worksheet: Worksheet = Depends(PurchasesWorksheetStub)
) -> BaseResponse:
    old_purchase = await PurchaseStats.get_or_none(purchase_key)
    if not old_purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Purchase {purchase_key} not found.'
        )

    purchase_row = build_purchase_row(request.purchase)
    try:
        update_row_by_key(worksheet, purchase_key, purchase_row)
        sort_by_column(worksheet, CREATE_TIME_COLUMN)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Fail to update row to worksheet: {e}'
        )

    await request.purchase.save()
    return SuccessResponse(detail=str(worksheet))


@purchases_router.delete('/{purchase_key}')
async def remove_purchase(
    purchase_key: str,
    worksheet: Worksheet = Depends(PurchasesWorksheetStub)
) -> BaseResponse:
    purchase = await PurchaseStats.get_or_none(purchase_key)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Purchase {purchase_key} not found.'
        )

    try:
        remove_row_by_key(worksheet, purchase_key)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Fail to update row at worksheet: {e}'
        )

    await purchase.delete()
    return SuccessResponse(detail=str(worksheet))
