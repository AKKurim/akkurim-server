from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class AthleteGuardian(BaseModel, table=True):
    __tablename__ = "athlete_guardian"

    athlete_id: UUID = Field(primary_key=True, foreign_key="athlete.id", index=True)
    guardian_id: UUID = Field(primary_key=True, foreign_key="guardian.id", index=True)
