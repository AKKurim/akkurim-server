from datetime import time
from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class TrainingTime(BaseModel, table=True):
    __tablename__ = "training_time"

    id: UUID = Field(primary_key=True, index=True)
    day: str = Field(nullable=False)
    summer_time: time = Field(nullable=False)
    winter_time: time = Field(nullable=False)
    duration_summer: int = Field(nullable=False)
    duration_winter: int = Field(nullable=False)
