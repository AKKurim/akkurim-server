from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Trainer(BaseModel, table=True):
    __tablename__ = "trainer"

    id: UUID = Field(primary_key=True, index=True)
    athlete_id: UUID = Field(nullable=False, foreign_key="athlete.id")
    bank_number: str | None = Field(default=None)
    status: str = Field(nullable=False)
    qualification: str = Field(nullable=False)
    salary_per_hour: int = Field(nullable=False)
