from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class GroupAthlete(BaseModel, table=True):
    __tablename__ = "group_athlete"

    group_id: UUID = Field(primary_key=True, foreign_key="group.id", index=True)
    athlete_id: UUID = Field(primary_key=True, foreign_key="athlete.id", index=True)
