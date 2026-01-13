from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class Response(BaseModel, table=True):
    __tablename__ = "response"

    id: UUID = Field(primary_key=True, index=True)
    request_id: UUID = Field(nullable=False)
    person_type: str = Field(nullable=False)
    person_id: UUID = Field(nullable=False)
    file_id: UUID | None = Field(default=None)
    description: str = Field(nullable=False)
