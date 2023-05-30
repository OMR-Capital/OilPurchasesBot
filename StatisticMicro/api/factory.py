from fastapi import FastAPI

from api.routers import root_router
from api.stubs import PurchasesRawWorksheetStub, PurchasesSortedWorksheetStub
from utils.init_worksheet import (init_purchases_raw_worksheet,
                                  init_purchases_sorted_worksheet)


def create_app() -> FastAPI:
    app = FastAPI(
        title='OilPurchases Statistic',
        version='0.1.0',
        root_path='/statistic'
    )
    app.include_router(root_router)
    app.dependency_overrides.update(
        {
            PurchasesRawWorksheetStub: init_purchases_raw_worksheet,
            PurchasesSortedWorksheetStub: init_purchases_sorted_worksheet,
        }
    )
    return app
