from typing import Any, Dict

from pydantic import UUID1, BaseModel


class SSEEvent(BaseModel):
    action: str
    table_name: str
    object_id: int | UUID1
    object_data: Dict[str, Any]
