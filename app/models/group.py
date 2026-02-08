from datetime import time
from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class GroupBase(SQLModel):
    __tablename__ = "group"

    name: str = Field(nullable=False)
    description: str | None = Field(default=None)

    school_year_id: UUID = Field(
        nullable=False, foreign_key="school_year.id", index=True
    )
    system: int | None = Field(default=None)

    day_of_week: str = Field(nullable=False)
    summer_time: time = Field(nullable=False)
    winter_time: time = Field(nullable=False)
    duration_summer: int = Field(nullable=False)
    duration_winter: int = Field(nullable=False)
    default_location_summer: str | None = Field(default=None)
    default_location_winter: str | None = Field(default=None)


class Group(GroupBase, BaseModel, table=True):
    __tablename__ = "group"
    id: UUID = Field(primary_key=True, index=True)


class GroupCreateUpdate(GroupBase):
    trainer_ids: list[UUID]
    athlete_ids: list[UUID]


class PersonSimple:
    id: UUID
    first_name: str
    last_name: str


class GroupReadDetail(GroupBase):
    id: UUID
    trainers: list[PersonSimple]
    athletes: list[PersonSimple]

    model_config = {"arbitrary_types_allowed": True}
