from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class ItemType(BaseModel, table=True):
    __tablename__ = "item_type"

    id: UUID = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    type: str = Field(nullable=False)
