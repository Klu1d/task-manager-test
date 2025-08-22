from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.infrastructure.configs import Config
from app.ioc import AppProvider
from app.presentation.api import task

config = Config()
container = make_async_container(AppProvider(), context={Config: config})


def get_fastapi_app() -> FastAPI:
    app = FastAPI()
    setup_dishka(container, app)
    app.include_router(task.router)
    return app


def app():
    fastapi_app = get_fastapi_app()
    return fastapi_app
