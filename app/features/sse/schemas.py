from enum import Enum
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel


class LocalActionEnum(Enum):
    upsert = "upsert"
    delete = "delete"


class SSEEvent(SQLModel):
    tenant: str
    table_name: str
    endpoint: Optional[str] = None
    http_method: str = "GET"
    local_action: LocalActionEnum = LocalActionEnum.upsert
    id: UUID | str | int
