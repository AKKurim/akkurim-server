from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Group(BaseModel, table=True):
    __tablename__ = "group"

    id: UUID = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    training_time_id: UUID = Field(nullable=False)
    school_year_id: UUID = Field(nullable=False)
    system: int | None = Field(default=None)
