from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class AthleteMeetEvent(BaseModel, table=True):
    __tablename__ = "athlete_meet_event"

    athlete_id: UUID = Field(primary_key=True)
    meet_event_id: UUID = Field(primary_key=True)
    result: str | None = Field(default=None)
    wind: str | None = Field(default=None)
    pb_sb: str | None = Field(default=None)
    points: str | None = Field(default=None)
    bib: str | None = Field(default=None)
