from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Meet(BaseModel, table=True):
    __tablename__ = "meet"

    id: UUID = Field(primary_key=True, index=True)
    type: str = Field(nullable=False)
    external_id: str | None = Field(default=None)
    name: str = Field(nullable=False)
    start_at: AwareDatetime = Field(
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )
    registration_start_at: AwareDatetime | None = Field(
        default=None,
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    end_at: AwareDatetime = Field(
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )
    registration_end_at: AwareDatetime | None = Field(
        default=None,
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    registration_limit: int | None = Field(default=None)
    location: str | None = Field(default=None)
    organizer: str | None = Field(default=None)
