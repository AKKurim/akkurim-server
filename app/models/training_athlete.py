from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class TrainingAthlete(BaseModel, table=True):
    __tablename__ = "training_athlete"

    training_id: UUID = Field(primary_key=True)
    athlete_id: UUID = Field(primary_key=True)
    presence: str = Field(nullable=False)
