from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Request(BaseModel, table=True):
    __tablename__ = "request"

    id: UUID = Field(primary_key=True, index=True)
    type: str = Field(nullable=False)
    status: str = Field(nullable=False)
    person_id: UUID = Field(nullable=False)
    item_id: UUID | None = Field(default=None, foreign_key="item.id", index=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
