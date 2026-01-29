from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Discipline(BaseModel, table=True):
    __tablename__ = "discipline"

    id: int = Field(primary_key=True)
    traditional: int | None = Field(default=None)
    discipline_type_id: int = Field(
        nullable=False, foreign_key="discipline_type.id", index=True
    )
    description: str = Field(nullable=False)
    short_description: str = Field(nullable=False)
    description_en: str = Field(nullable=False)
    short_description_en: str = Field(nullable=False)
