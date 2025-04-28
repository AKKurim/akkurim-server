from datetime import datetime

import orjson
from asyncpg import Connection
from pydantic import UUID1

from app.core.sse.broadcast import broadcast as global_broadcast
from app.core.sse.schemas import LocalActionEnum, SSEEvent
from app.core.utils.default_service import DefaultService
from app.core.utils.sql_utils import (
    convert_uuid_to_str,
    generate_sql_insert_with_returning,
    generate_sql_read,
    generate_sql_read_with_join_table,
)
from app.features.meet.schemas import MeetEventRead


class MeetEventService(DefaultService):
    def __init__(self):
        super().__init__(
            "meet_event",
            "/meet_event/{id}",
            MeetEventRead,
        )

    async def get_meet_events_by_meet_id(
        self,
        tenant_id: str,
        meet_id: str,
        db: Connection,
    ) -> list[MeetEventRead]:
        query, values = generate_sql_read(
            tenant_id=tenant_id,
            table=self.table,
            columns=self.read_model.model_fields.keys(),
            conditions={
                "meet_id": {
                    "value": meet_id,
                    "operator": "=",
                }
            },
        )
        result = await db.fetch(query, *values)
        return (
            [MeetEventRead(**convert_uuid_to_str(row)) for row in result]
            if result
            else []
        )
