from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Athlete(BaseModel, table=True):
    __tablename__ = "athlete"

    id: UUID = Field(primary_key=True, index=True)
    bank_number: str | None = Field(default=None)
    birth_number: str = Field(nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    street: str = Field(nullable=False)
    city: str = Field(nullable=False)
    zip: str = Field(nullable=False)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    ean: str | None = Field(default=None)
    note: str | None = Field(default=None)
    club_id: str | None = Field(default=None, foreign_key="club.id", index=True)
    profile_image_id: UUID | None = Field(
        default=None, foreign_key="file.id", index=True
    )
    status: str = Field(nullable=False)
