from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Category(BaseModel, table=True):
    __tablename__ = "category"

    id: int = Field(primary_key=True)
    sex: int = Field(nullable=False)
    description: str = Field(nullable=False)
    short_description: str = Field(nullable=False)
    description_en: str = Field(nullable=False)
    short_description_en: str = Field(nullable=False)
    age: str | None = Field(default=None)
