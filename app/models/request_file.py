from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class RequestFile(BaseModel, table=True):
    __tablename__ = "request_file"

    request_id: UUID = Field(primary_key=True, foreign_key="request.id", index=True)
    file_id: UUID = Field(primary_key=True, foreign_key="file.id", index=True)
