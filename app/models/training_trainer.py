from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class TrainingTrainer(BaseModel, table=True):
    __tablename__ = "training_trainer"

    training_id: UUID = Field(primary_key=True, foreign_key="training.id", index=True)
    trainer_id: UUID = Field(primary_key=True, foreign_key="trainer.id", index=True)
    presence: str | None = Field(default=None)
