from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class File(BaseModel, table=True):
    __tablename__ = "file"

    id: UUID = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    size: int = Field(nullable=False)
    mime_type: str = Field(nullable=False)
    type: str = Field(nullable=False)
