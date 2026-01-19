from datetime import datetime, timezone

import sqlalchemy as sa
from pydantic import AwareDatetime, field_validator, model_validator
from sqlalchemy.orm import declared_attr
from sqlmodel import DateTime, Field, SQLModel


class BaseModel(SQLModel, table=False):
    """Base mixin for models.

    Uses `declared_attr` to provide a fresh SQLAlchemy `Column` for each
    subclass (avoids Column re-use errors), while keeping Pydantic-like
    defaults via a root validator so model instances get sensible Python
    timestamps when not provided.
    """

    created_at: AwareDatetime = Field(sa_type=DateTime(timezone=True), nullable=False)
    updated_at: AwareDatetime = Field(sa_type=DateTime(timezone=True), nullable=False)
    deleted_at: AwareDatetime | None = Field(
        sa_type=DateTime(timezone=True), nullable=True
    )
    last_updated_by: str | None = None

    @model_validator(mode="before")
    def _set_default_timestamps(cls, values: dict):
        now = datetime.now(timezone.utc)
        values.setdefault("created_at", now)
        values.setdefault("updated_at", now)
        # `deleted_at` intentionally left as-is (None by default)
        return values

    @field_validator("created_at", "updated_at", "deleted_at", mode="after")
    @classmethod
    def _ensure_timezone(cls, v):
        if v is None:
            return v
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        try:
            return v.astimezone(timezone.utc)
        except Exception:
            return v

    class Config:
        validate_assignment = True
