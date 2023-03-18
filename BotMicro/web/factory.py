from aiogram import Bot, Dispatcher
from deta import Deta  # type: ignore
from fastapi import FastAPI

from web.stubs import BotStub, DispatcherStub, SecretStub
from web.routes.webhook import webhook_router
from web.routes.actions import actions_router


def create_app(deta: Deta, bot: Bot, dispatcher: Dispatcher, webhook_secret: str) -> FastAPI:
    app = FastAPI()

    app.dependency_overrides.update(
        {
            BotStub: lambda: bot,
            DispatcherStub: lambda: dispatcher,
            SecretStub: lambda: webhook_secret,
        }
    )

    app.include_router(webhook_router)
    app.include_router(actions_router)
    return app
