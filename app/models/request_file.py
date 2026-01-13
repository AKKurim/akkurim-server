from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class RequestFile(BaseModel, table=True):
    __tablename__ = "request_file"

    request_id: UUID = Field(primary_key=True)
    file_id: UUID = Field(primary_key=True)
