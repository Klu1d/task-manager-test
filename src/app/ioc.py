from typing import AsyncIterable
from uuid import uuid4

from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application import interfaces
from app.application.interactors import GetAllTaskInteractor, GetTaskInteractor, NewTaskInteractor, RemoveTaskInteractor, UpdateTaskInteractor
from app.infrastructure.configs import Config
from app.infrastructure.providers import get_sessionmaker
from app.infrastructure.gateways import TaskGateway


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return get_sessionmaker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, interfaces.DBSession]]:
        async with session_maker() as session:
            yield session

    task_gateway = provide(
        TaskGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.TaskReader, interfaces.TaskSaver],
    )

    get_all_tasks_interactor = provide(GetAllTaskInteractor, scope=Scope.REQUEST)
    get_task_interactor = provide(GetTaskInteractor, scope=Scope.REQUEST)
    new_task_interactor = provide(NewTaskInteractor, scope=Scope.REQUEST)
    update_task_interactor = provide(UpdateTaskInteractor, scope=Scope.REQUEST)
    remove_task_interactor = provide(RemoveTaskInteractor, scope=Scope.REQUEST)