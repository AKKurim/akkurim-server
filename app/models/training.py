from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Training(BaseModel, table=True):
    __tablename__ = "training"

    id: UUID = Field(primary_key=True, index=True)
    start_at: AwareDatetime = Field(
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )
    group_id: UUID = Field(nullable=False)
    description: str | None = Field(default=None)
    duration_minutes: int = Field(nullable=False)
