from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Guardian(BaseModel, table=True):
    __tablename__ = "guardian"

    id: UUID = Field(primary_key=True, index=True)
    bank_number: str | None = Field(default=None)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    phone: str | None = Field(default=None)
