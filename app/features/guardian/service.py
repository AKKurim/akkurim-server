from datetime import datetime

from asyncpg import Connection
from pydantic import UUID1

from app.core.shared.exceptions import AlreadyExistsError, UniqueViolationErrorHTTP
from app.core.utils.default_service import DefaultService
from app.core.utils.sql_utils import convert_uuid_to_str
from app.features.guardian.schemas import GuardianCreate, GuardianRead, GuardianUpdate


class GuardianService(DefaultService):
    def __init__(self):
        super().__init__(
            "guardian",
            "/guardian/{id}",
            GuardianRead,
        )

    async def get_guardian_by_id(
        self,
        tenant_id: str,
        guardian_id: UUID1,
        db: Connection,
    ) -> GuardianRead:
        return await super().get_object_by_id(
            tenant_id,
            guardian_id,
            db,
        )

    async def create_guardian(
        self,
        tenant_id: str,
        guardian: GuardianCreate,
        athlete_id: UUID1,
        db: Connection,
    ) -> GuardianRead:
        try:
            res = await super().create_object(
                tenant_id,
                guardian,
                db,
            )
        except (UniqueViolationErrorHTTP, AlreadyExistsError):
            res = await db.fetchrow(
                f"SELECT * FROM {tenant_id}.guardian WHERE email = $1",
                guardian["email"],
            )
            res = dict(res)
        await db.execute(
            f"INSERT INTO {tenant_id}.athlete_guardian (guardian_id, athlete_id) VALUES ($1, $2)",
            res["id"],
            athlete_id,
        )
        return convert_uuid_to_str(dict(res))

    async def update_guardian(
        self,
        tenant_id: str,
        guardian: GuardianUpdate,
        db: Connection,
    ) -> GuardianRead:
        return await super().update_object(
            tenant_id,
            guardian,
            db,
        )

    async def delete_guardian(
        self,
        tenant_id: str,
        guardian_id: UUID1,
        db: Connection,
    ) -> None:
        return await super().delete_object(
            tenant_id,
            guardian_id,
            db,
        )

    async def get_all_guardians(
        self, tenant_id: str, db: Connection
    ) -> list[GuardianRead]:
        return await super().get_all_objects(tenant_id, db)

    async def get_all_guardians_updated_after(
        self,
        tenant_id: str,
        last_updated: datetime,
        db: Connection,
    ) -> list[GuardianRead]:
        return await super().get_all_objects_updated_after(
            tenant_id,
            last_updated,
            db,
        )
