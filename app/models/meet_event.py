from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class MeetEvent(BaseModel, table=True):
    __tablename__ = "meet_event"

    id: UUID = Field(primary_key=True, index=True)
    meet_id: UUID = Field(nullable=False)
    discipline_id: int = Field(nullable=False)
    category_id: int = Field(nullable=False)
    start_at: AwareDatetime = Field(
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )
    phase: str | None = Field(default=None)
    count: int | None = Field(default=None)
