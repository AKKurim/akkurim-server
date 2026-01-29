from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class GroupTrainer(BaseModel, table=True):
    __tablename__ = "group_trainer"

    group_id: UUID = Field(primary_key=True, foreign_key="group.id", index=True)
    trainer_id: UUID = Field(primary_key=True, foreign_key="trainer.id", index=True)
