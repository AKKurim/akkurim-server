from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class SignUpFormGroup(BaseModel, table=True):
    __tablename__ = "sign_up_form_group"

    sign_up_form_id: UUID = Field(primary_key=True)
    group_id: UUID = Field(primary_key=True)
