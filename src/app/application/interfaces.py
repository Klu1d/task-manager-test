from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.entities import Task


class TaskSaver(Protocol):
    @abstractmethod
    async def save(self, task: Task) -> None: ...

    @abstractmethod
    async def delete(self, uuid: str) -> None: ...


class TaskReader(Protocol):
    @abstractmethod
    async def all(self) -> list[Task]: ...

    @abstractmethod
    async def read_by_uuid(self, uuid: str) -> Task | None: ...

    @abstractmethod
    async def read_by_title(self, title: str) -> Task | None: ...


class UUIDGenerator(Protocol):
    def __call__(self) -> UUID: ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...