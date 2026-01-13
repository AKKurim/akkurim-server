from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class AthleteSignUpForm(BaseModel, table=True):
    __tablename__ = "athlete_sign_up_form"

    athlete_id: UUID = Field(primary_key=True)
    sign_up_form_id: UUID = Field(primary_key=True)
