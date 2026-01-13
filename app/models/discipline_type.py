from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class DisciplineType(BaseModel, table=True):
    __tablename__ = "discipline_type"

    id: int = Field(primary_key=True)
    sort: str = Field(nullable=False)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    name_en: str | None = Field(default=None)
    description_en: str | None = Field(default=None)
