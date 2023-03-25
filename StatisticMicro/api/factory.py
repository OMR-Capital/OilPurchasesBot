from fastapi import FastAPI

from api.routers import root_router
from api.stubs import WorksheetStub
from utils.init_worksheet import init_applications_worksheet


def create_app() -> FastAPI:
    app = FastAPI(
        title='OilPurchases Statistic',
        version='0.1.0',
        root_path='/statistic'
    )
    app.include_router(root_router)
    app.dependency_overrides.update(
        {
            WorksheetStub: init_applications_worksheet
        }
    )
    return app
