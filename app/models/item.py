from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Item(BaseModel, table=True):
    __tablename__ = "item"

    id: UUID = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    image_id: UUID | None = Field(default=None, foreign_key="file.id", index=True)
    count: int = Field(nullable=False)
    item_type_id: UUID = Field(nullable=False, foreign_key="item_type.id", index=True)
    athlete_id: UUID | None = Field(default=None, foreign_key="athlete.id", index=True)
