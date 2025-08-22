from datetime import datetime, timezone

from app.application.dto import TaskDTO
from app.application.interfaces import DBSession, TaskReader, TaskSaver, UUIDGenerator
from app.domain.entities import Status, Task


class GetAllTaskInteractor:
    def __init__(self, gateway: TaskReader):
        self._gateway = gateway

    async def __call__(self) -> list[Task]:
        return await self._gateway.all()


class GetTaskInteractor:
    def __init__(self, gateway: TaskReader):
        self._gateway = gateway

    async def __call__(self, uuid: str) -> Task | None:
        return await self._gateway.read_by_uuid(uuid)


class NewTaskInteractor:
    def __init__(
        self,
        gateway: TaskSaver,
        uuid_generator: UUIDGenerator,
        session: DBSession,
    ):
        self._gateway = gateway
        self._uuid_generator = uuid_generator
        self._session = session

    async def __call__(self, dto: TaskDTO) -> Task | None:
        uuid = str(self._uuid_generator())
        task = Task(
            uuid=uuid,
            title=dto.title,
            description=dto.description,
            status=Status.CREATED,
            created_at=datetime.now(timezone.utc),
        )
        await self._gateway.save(task)
        await self._session.commit()
        return task


class UpdateTaskInteractor:
    def __init__(
        self,
        gateway_saver: TaskSaver,
        gateway_reader: TaskReader,
        session: DBSession,
    ):
        self._gateway_saver = gateway_saver
        self._gateway_reader = gateway_reader
        self._session = session

    async def __call__(self, uuid: str, status: str, dto: TaskDTO) -> Task | None:
        task = await self._gateway_reader.read_by_uuid(uuid)
        if task is None:
            return None

        if dto.title:
            task.title = dto.title
        if dto.description:
            task.description = dto.description
        if status:
            task.status = status
        task.updated_at = datetime.now(timezone.utc)

        await self._session.commit()
        return task


class RemoveTaskInteractor:
    def __init__(
        self,
        gateway_saver: TaskSaver,
        gateway_reader: TaskReader,
        session: DBSession,
    ):
        self._gateway_saver = gateway_saver
        self._gateway_reader = gateway_reader
        self._session = session

    async def __call__(self, uuid: str) -> bool | None:
        task = await self._gateway_reader.read_by_uuid(uuid)
        if task is None:
            return None

        await self._gateway_saver.delete(uuid)
        await self._session.commit()
        return True
