from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Payment(BaseModel, table=True):
    __tablename__ = "payment"

    id: int = Field(primary_key=True)
    type: str = Field(nullable=False)
    amount: float = Field(nullable=False)
    status: str = Field(nullable=False)
    from_id: UUID | None = Field(default=None)
    to_id: UUID | None = Field(default=None)
    description: str | None = Field(default=None)
