from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class RemoteConfig(BaseModel, table=True):
    __tablename__ = "remote_config"

    id: int = Field(primary_key=True, index=True)
    urgent_message: str | None = Field(default=None)
    show_from: AwareDatetime = Field(
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )
    show_to: AwareDatetime = Field(
        sa_column=sa.Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )
    minimum_app_version: str = Field(nullable=False)
