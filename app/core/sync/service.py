from datetime import datetime, timezone

from asyncpg import Connection
from pydantic import AwareDatetime
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.logging import logger
from app.core.utils.sql_utils import (
    convert_uuid_to_str,
    generate_sql_insert,
    generate_sql_read,
    generate_sql_tables_updated_after,
)
from app.models import BaseModel, models_by_table_name


class SyncService:
    def __init__(self):
        pass

    async def get_tables_to_sync(
        self,
        tenant_id: str,
        from_date: AwareDatetime,
        db: AsyncSession,
    ) -> list[str]:
        query = generate_sql_tables_updated_after(
            tenant_id=tenant_id,
            table_names=models_by_table_name.keys(),
        )
        res = await db.exec(text(query), from_date)
        return [r["table_name"] for r in res]

    async def get_objects_to_sync(
        self,
        tenant_id: str,
        table_name: str,
        from_date: AwareDatetime,
        db: Connection,
    ) -> list[BaseModel]:
        try:
            schema: BaseModel = models_by_table_name[table_name]
        except KeyError:
            raise ValueError(f"Table {table_name} not found in TABLE_NAMES")

        query, values = generate_sql_read(
            tenant_id=tenant_id,
            table=table_name,
            columns=schema.model_fields.keys(),
            conditions={
                "updated_at": {
                    "value": from_date,
                    "operator": ">=",
                },
                "deleted_at": {
                    "value": from_date,
                    "operator": ">=",
                },
            },
            condition_operator="OR",
        )
        res = await db.fetch(query, *values)
        return [convert_uuid_to_str(dict(r)) for r in res]

    async def sync_objects(
        self,
        tenant_id: str,
        table_name: str,
        data: list[BaseModel],
        primary_keys: list[str],
        db: Connection,
    ) -> None:
        try:
            schema: BaseModel = models_by_table_name[table_name]
        except KeyError:
            raise ValueError(f"Table {table_name} not found in TABLE_NAMES")
        for d in data:
            d = schema(**d)
            d = d.dict(exclude_unset=True)
            # IMPORTANT: ensure updated_at is set to server timestamp
            # due to sync implementation in the frontend (only sync objects after the last sync)
            d["updated_at"] = datetime.now(timezone.utc)
            query, values = generate_sql_insert(
                tenant_id=tenant_id,
                table=table_name,
                data=d,
            )
            query = query[:-1]  # remove semicolon
            query += f" ON CONFLICT ({', '.join(primary_keys)}) DO UPDATE SET "
            query += ", ".join(
                f"{col} = EXCLUDED.{col}"
                for col in schema.model_fields.keys()
                if col != "id"
            )
            query += ";"
            logger.info(query)
            await db.execute(query, *values)

        return None
