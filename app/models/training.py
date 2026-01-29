from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class TrainingBase(SQLModel):
    start_at: AwareDatetime = Field(
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )
    duration_minutes: int = Field(nullable=False)
    group_id: UUID = Field(nullable=False, foreign_key="group.id", index=True)
    description: str | None = Field(default=None)

    location: str | None = Field(nullable=True)
    training_type: str | None = Field(nullable=True)
    attendance_taken_at: AwareDatetime | None = Field(
        default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=True)
    )
    cancelled_reason: str | None = Field(default=None)


class Training(BaseModel, TrainingBase, table=True):
    __tablename__ = "training"

    id: UUID = Field(primary_key=True, index=True)


class TrainingDashboardRead(TrainingBase):
    id: UUID
    group_name: str
    attendee_count: int
