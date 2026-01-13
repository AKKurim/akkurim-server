from datetime import datetime, timezone

import sqlalchemy as sa
from pydantic import root_validator, validator
from sqlalchemy.orm import declared_attr
from sqlmodel import DateTime, SQLModel


class BaseModel(SQLModel):
    """Base mixin for models.

    Uses `declared_attr` to provide a fresh SQLAlchemy `Column` for each
    subclass (avoids Column re-use errors), while keeping Pydantic-like
    defaults via a root validator so model instances get sensible Python
    timestamps when not provided.
    """

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    last_updated_by: str | None = None

    @declared_attr
    def created_at(cls):
        return sa.Column(
            DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        )

    @declared_attr
    def updated_at(cls):
        return sa.Column(
            DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        )

    @declared_attr
    def deleted_at(cls):
        return sa.Column(DateTime(timezone=True), nullable=True)

    @root_validator(pre=True)
    def _set_default_timestamps(cls, values):
        now = datetime.now(timezone.utc)
        values.setdefault("created_at", now)
        values.setdefault("updated_at", now)
        # `deleted_at` intentionally left as-is (None by default)
        return values

    @validator("created_at", "updated_at", "deleted_at", pre=False, always=False)
    def _ensure_timezone(cls, v):
        if v is None:
            return v
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        try:
            return v.astimezone(timezone.utc)
        except Exception:
            return v
