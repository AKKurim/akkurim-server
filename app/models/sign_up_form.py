from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class SignUpForm(BaseModel, table=True):
    __tablename__ = "sign_up_form"

    id: UUID = Field(primary_key=True, index=True)
    birth_number: str = Field(nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    street: str = Field(nullable=False)
    city: str = Field(nullable=False)
    zip: str = Field(nullable=False)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    guardian_first_name1: str = Field(nullable=False)
    guardian_last_name1: str = Field(nullable=False)
    guardian_first_name2: str | None = Field(default=None)
    guardian_last_name2: str | None = Field(default=None)
    guardian_phone1: str = Field(nullable=False)
    guardian_email1: str = Field(nullable=False)
    guardian_phone2: str | None = Field(default=None)
    guardian_email2: str | None = Field(default=None)
    note: str | None = Field(default=None)
    status: str = Field(nullable=False)
    school_year_id: UUID = Field(
        nullable=False, foreign_key="school_year.id", index=True
    )
    times_per_week: int = Field(nullable=False)
    days_in_week: str = Field(nullable=False)
