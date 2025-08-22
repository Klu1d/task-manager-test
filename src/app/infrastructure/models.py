from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.domain.entities import Status


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    uuid: Mapped[str] = mapped_column(
        "uuid",
        sa.Uuid,
        primary_key=True,
    )
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[Status] = mapped_column(
        sa.Enum(Status, name="task_status"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc)
    )
