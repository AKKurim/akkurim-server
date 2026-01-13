from datetime import date
from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Helper(BaseModel, table=True):
    __tablename__ = "helper"

    id: UUID = Field(primary_key=True, index=True)
    status: str = Field(nullable=False)
    bank_number: str | None = Field(default=None)
    first_name: str = Field(nullable=False)
    lats_name: str = Field(nullable=False)
    date_of_birth: date | None = Field(default=None)
    email: str = Field(nullable=False)
    phone: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    zip: str | None = Field(default=None)
    qualification: str | None = Field(default=None)
    preferrence: str | None = Field(default=None)
