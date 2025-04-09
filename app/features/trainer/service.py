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
)
from app.features.trainer.schemas import (
    TrainerCreate,
    TrainerRead,
    TrainerStatusRead,
    TrainerUpdate,
)


class TrainerService(DefaultService):
    def __init__(self):
        super().__init__(
            table_name="trainer",
            broadcast_endpoint="/trainer/{id}",
            read_model=TrainerRead,
        )

    async def get_trainer_by_id(
        self,
        tenant_id: str,
        trainer_id: UUID1,
        db: Connection,
    ) -> TrainerRead:
        return await super().get_object_by_id(
            tenant_id,
            trainer_id,
            db,
        )

    async def create_trainer(
        self,
        tenant_id: str,
        trainer: TrainerCreate,
        db: Connection,
    ) -> TrainerRead:
        return await super().create_object(
            tenant_id,
            trainer,
            db,
        )

    async def update_trainer(
        self,
        tenant_id: str,
        trainer: TrainerUpdate,
        db: Connection,
    ) -> TrainerRead:
        return await super().update_object(
            tenant_id,
            trainer,
            db,
        )

    async def delete_trainer(
        self,
        tenant_id: str,
        trainer_id: UUID1,
        db: Connection,
    ) -> TrainerRead:
        return await super().delete_object(
            tenant_id,
            trainer_id,
            db,
        )

    async def get_all_trainers(
        self,
        tenant_id: str,
        db: Connection,
    ) -> list[TrainerRead]:
        return await super().get_all_objects(
            tenant_id,
            db,
        )

    async def get_all_statuses(
        self,
        tenant_id: str,
        db: Connection,
    ) -> list[TrainerStatusRead]:
        query, values = generate_sql_read(
            tenant_id,
            "trainer_status",
            TrainerStatusRead.model_fields.keys(),
        )
        res = await db.fetch(query, *values)
        return [convert_uuid_to_str(dict(r)) for r in res]

    async def create_status(
        self,
        tenant_id: str,
        status: TrainerStatusRead,
        db: Connection,
    ) -> TrainerStatusRead:
        query, values = generate_sql_insert_with_returning(
            tenant_id,
            "trainer_status",
            status,
            TrainerStatusRead.model_fields.keys(),
        )
        res = await db.fetchrow(query, *values)

        event = SSEEvent(
            tenant_id=tenant_id,
            table_name="trainer_status",
            endpoint="/trainer/status/",  # update all statuses since it we dont have a specific endpoint
            local_action=LocalActionEnum.upsert,
            id=str(res["id"]),
        )
        await global_broadcast.publish(
            channel="update",
            message=orjson.dumps(event.model_dump()).decode("utf-8"),
        )

        return convert_uuid_to_str(dict(res))
