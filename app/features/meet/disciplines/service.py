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
from app.features.meet.schemas import (
    DisciplineCreate,
    DisciplineRead,
    DisciplineTypeCreate,
    DisciplineTypeRead,
    DisciplineUpdate,
)


class DisciplineService(DefaultService):
    def __init__(self):
        super().__init__(
            "discipline",
            "/discipline/{id}",
            DisciplineRead,
        )

    async def get_discipline_by_id(
        self,
        tenant_id: str,
        discipline_id: int,
        db: Connection,
    ) -> DisciplineRead:
        return await super().get_object_by_id(
            tenant_id,
            discipline_id,
            db,
        )

    async def create_discipline(
        self,
        tenant_id: str,
        discipline: DisciplineCreate,
        db: Connection,
    ) -> DisciplineRead:
        return await super().create_object(
            tenant_id,
            discipline,
            db,
        )

    async def update_discipline(
        self,
        tenant_id: str,
        discipline: DisciplineUpdate,
        db: Connection,
    ) -> DisciplineRead:
        return await super().update_object(
            tenant_id,
            discipline,
            db,
        )

    async def delete_discipline(
        self,
        tenant_id: str,
        discipline_id: int,
        db: Connection,
    ) -> DisciplineRead:
        return await super().delete_object(
            tenant_id,
            discipline_id,
            db,
        )

    async def get_all_disciplines(
        self,
        tenant_id: str,
        db: Connection,
    ) -> list[DisciplineRead]:
        return await super().get_all_objects(tenant_id, db)

    async def get_all_discipline_types(
        self,
        tenant_id: str,
        db: Connection,
    ) -> list[DisciplineTypeRead]:
        query, values = generate_sql_read(
            tenant_id,
            "discipline_type",
            DisciplineTypeRead.model_fields.keys(),
        )
        res = await db.fetch(query, *values)
        return [(dict(row)) for row in res]

    async def create_discipline_type(
        self,
        tenant_id: str,
        discipline_type: DisciplineTypeCreate,
        db: Connection,
    ) -> DisciplineTypeRead:
        query, values = generate_sql_insert_with_returning(
            tenant_id,
            "discipline_type",
            discipline_type,
            DisciplineTypeRead.model_fields.keys(),
        )
        res = await db.fetch(query, *values)

        event = SSEEvent(
            tenant=tenant_id,
            table_name="discipline_type",
            endpoint="/discipline/type/",  # update all statuses since it we dont have a specific endpoint
            local_action=LocalActionEnum.upsert,
            id=str(discipline_type["id"]),
        )
        await global_broadcast.publish(
            channel="update",
            message=orjson.dumps(event.model_dump()).decode("utf-8"),
        )

        return dict(res)
