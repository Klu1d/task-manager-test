from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class Status(StrEnum):
    CREATED = "CREATED"
    WORKING = "WORKING"
    COMPLETED = "COMPLETED"


@dataclass(slots=True)
class Task:
    uuid: str
    title: str
    description: int
    status: Status
    created_at: datetime
    updated_at: datetime | None = None
