from datetime import datetime

from asyncpg import Connection
from pydantic import UUID1

from app.core.utils.default_service import DefaultService
from app.core.utils.sql_utils import (
    convert_uuid_to_str,
    generate_sql_read,
    generate_sql_read_with_join_table,
)
from app.features.athlete.schemas import (
    AthleteCreate,
    AthleteRead,
    AthleteStatusRead,
    AthleteUpdate,
)
from app.features.guardian.schemas import GuardianRead


class AthleteService(DefaultService):
    def __init__(self):
        super().__init__(
            "athlete",
            "/athlete/{id}",
            AthleteRead,
        )

    async def get_athlete_by_id(
        self,
        tenant_id: str,
        athlete_id: UUID1,
        db: Connection,
    ) -> AthleteRead:
        return await super().get_object_by_id(
            tenant_id,
            athlete_id,
            db,
        )

    async def create_athlete(
        self,
        tenant_id: str,
        athlete: AthleteCreate,
        db: Connection,
    ) -> AthleteRead:
        return await super().create_object(
            tenant_id,
            athlete,
            db,
        )

    async def update_athlete(
        self,
        tenant_id: str,
        athlete: AthleteUpdate,
        db: Connection,
    ) -> AthleteRead:
        return await super().update_object(
            tenant_id,
            athlete,
            db,
        )

    async def delete_athlete(
        self,
        tenant_id: str,
        athlete_id: UUID1,
        db: Connection,
    ) -> None:
        return await super().delete_object(
            tenant_id,
            athlete_id,
            db,
        )

    async def get_all_athletes(
        self, tenant_id: str, db: Connection
    ) -> list[AthleteRead]:
        return await super().get_all_objects(tenant_id, db)

    async def get_all_athletes_updated_after(
        self,
        tenant_id: str,
        last_updated_at: datetime,
        db: Connection,
    ) -> list[AthleteRead]:
        return await super().get_all_objects_updated_after(
            tenant_id, last_updated_at, db
        )

    async def get_all_statuses(
        self, tenant_id: str, db: Connection
    ) -> list[AthleteStatusRead]:
        query, values = generate_sql_read(
            tenant_id,
            "athlete_status",
            AthleteStatusRead.model_fields.keys(),
        )
        res = db.fetch(query, *values)
        return convert_uuid_to_str(dict(res))

    async def get_guardians_for_athlete(
        self, tenant_id: str, athlete_id: UUID1, db: Connection
    ) -> list[dict]:
        query, values = generate_sql_read_with_join_table(
            tenant_id,
            "guardian",
            GuardianRead.model_fields.keys(),
            "athlete_guardian",
            {
                "guardian.id": {
                    "direct_value": f"{tenant_id}.athlete_guardian.guardian_id"
                }
            },
            {"athlete_guardian.athlete_id": {"value": athlete_id}},
        )
        res = await db.fetch(query, *values)
        return convert_uuid_to_str(dict(res))
