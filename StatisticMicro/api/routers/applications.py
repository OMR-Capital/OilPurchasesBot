from fastapi import APIRouter, Depends, HTTPException, status
from gspread.worksheet import Worksheet

from api.schemas.applications import ApplicationRequest
from api.schemas.base import BaseResponse, FailureResponse, SuccessResponse
from api.stubs import WorksheetStub
from google_sheets_utils.worksheet import add_application_row, clear_application_row, update_application_row
from models.application import Application
from sheet_data_utils.applications import build_application_row

applications_router = APIRouter(prefix='/application', tags=['Applications'])


@applications_router.post('/')
async def add_application(
    request: ApplicationRequest,
    worksheet: Worksheet = Depends(WorksheetStub)
) -> BaseResponse:
    pass
    # if not request.application.key:
    #     return FailureResponse(detail=f'Application key must be specified')

    # application = await Application.get_or_none(request.application.key)
    # if application:
    #     return FailureResponse(detail=f'Application {application.key} already exists')

    # try:
    #     application = await fetch_application_from_backend(request.application)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f'Fail to fetch application data from backend: {e}'
    #     )

    # application_row = build_application_row(application)
    # try:
    #     add_application_row(worksheet, application_row)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f'Fail to append row to worksheet: {e}'
    #     )

    # await application.save()
    # return SuccessResponse(detail=str(worksheet))


@applications_router.patch('/{app_key}')
async def update_application(
    app_key: str,
    request: ApplicationRequest,
    worksheet: Worksheet = Depends(WorksheetStub)
) -> BaseResponse:
    pass
    # application = await Application.get_or_none(app_key)
    # if not application:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f'Application {app_key} not found.'
    #     )

    # try:
    #     fetched_application = await fetch_application_from_backend(request.application)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f'Fail to fetch application data from backend: {e}'
    #     )

    # fetched_application.key = app_key

    # application_row = build_application_row(fetched_application)
    # try:
    #     update_application_row(worksheet, application.key, application_row)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f'Fail to update row at worksheet: {e}'
    #     )

    # await fetched_application.save()
    # return SuccessResponse(detail=str(worksheet))


@applications_router.delete('/{app_key}')
async def remove_application(
    app_key: str,
    worksheet: Worksheet = Depends(WorksheetStub)
) -> BaseResponse:
    pass
    # application = await Application.get_or_none(app_key)
    # if not application:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f'Application {app_key} not found.'
    #     )

    # try:
    #     clear_application_row(worksheet, app_key)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f'Fail to update row at worksheet: {e}'
    #     )

    # await application.delete()
    # return SuccessResponse(detail=str(worksheet))
