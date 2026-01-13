from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class WebPost(BaseModel, table=True):
    __tablename__ = "web_post"

    id: UUID = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)
    cover_image_id: UUID | None = Field(default=None)
    content: str = Field(nullable=False)
    trainer_id: UUID = Field(nullable=False)
