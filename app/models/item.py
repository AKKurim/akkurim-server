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
    image_id: UUID | None = Field(default=None)
    count: int = Field(nullable=False)
    item_type_id: UUID = Field(nullable=False)
    athlete_id: UUID | None = Field(default=None)
