from datetime import datetime

from pydantic import BaseModel



class TaskRequest(BaseModel):
    title: str
    description: str


class TaskResponse(BaseModel):
    uuid: str
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime | None
