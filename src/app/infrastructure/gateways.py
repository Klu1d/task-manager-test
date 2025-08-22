from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.application.interfaces import TaskReader, TaskSaver
from app.domain.entities import Task


class TaskGateway(TaskReader, TaskSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_by_uuid(self, uuid: str) -> Task | None:
        query = text("SELECT * FROM tasks WHERE uuid = :uuid")
        result = await self._session.execute(
            statement=query,
            params={"uuid": uuid},
        )
        row = result.fetchone()
        if not row:
            return None
        return Task(
            uuid=row.uuid,
            title=row.title,
            description=row.description,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def read_by_title(self, title: str) -> Task | None:
        query = text("SELECT * FROM tasks WHERE title = :title")
        result = await self._session.execute(
            statement=query,
            params={"title": title},
        )
        row = result.fetchone()
        if not row:
            return None
        return Task(
            uuid=row.uuid,
            title=row.title,
            description=row.description,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def all(self) -> list[Task]:
        query = text("SELECT * FROM tasks")
        result = await self._session.execute(query)
        rows = result.mappings().all()
        return [
            Task(
                uuid=str(row.uuid),
                title=row.title,
                description=row.description,
                status=row.status,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]

    async def save(self, task: Task) -> None:
        query = text(
            "INSERT INTO tasks (uuid, title, description, status, created_at, updated_at) VALUES (:uuid, :title, :description, :status, :created_at, :updated_at)"
        )
        await self._session.execute(
            statement=query,
            params={
                "uuid": task.uuid,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
            },
        )

    async def delete(self, task_id: str) -> None:
        query = text("DELETE FROM tasks WHERE uuid = :uuid")
        await self._session.execute(
            statement=query,
            params={"uuid": task_id},
        )
