from enum import Enum
from typing import Optional

from pydantic import UUID1

from app.core.shared.base_schema import BaseSchema


class LocalActionEnum(Enum):
    upsert = "upsert"
    delete = "delete"


class SSEEvent(BaseSchema):
    tenant: str
    table_name: str
    endpoint: Optional[str] = None
    http_method: str = "GET"
    local_action: LocalActionEnum = LocalActionEnum.upsert
    id: UUID1 | str | int
