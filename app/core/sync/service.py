from asyncpg import Connection
from pydantic import AwareDatetime

from app.core.logging import logger
from app.core.shared.base_schema import BaseSchema
from app.core.sync.sync_config import TABLE_NAMES
from app.core.utils.sql_utils import (
    convert_uuid_to_str,
    generate_sql_insert,
    generate_sql_read,
    generate_sql_tables_updated_after,
)


class SyncService:
    def __init__(self):
        pass

    async def get_tables_to_sync(
        self,
        tenant_id: str,
        from_date: AwareDatetime,
        db: Connection,
    ) -> list[str]:
        query = generate_sql_tables_updated_after(
            tenant_id=tenant_id,
            table_names=TABLE_NAMES.keys(),
        )
        res = await db.fetch(query, from_date)
        return [r["table_name"] for r in res]

    async def get_objects_to_sync(
        self,
        tenant_id: str,
        table_name: str,
        from_date: AwareDatetime,
        db: Connection,
    ) -> list[BaseSchema]:
        try:
            schema: BaseSchema = TABLE_NAMES[table_name]
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
        data: list[BaseSchema],
        db: Connection,
    ) -> None:
        try:
            schema: BaseSchema = TABLE_NAMES[table_name]
        except KeyError:
            raise ValueError(f"Table {table_name} not found in TABLE_NAMES")
        for d in data:
            d = schema(**d)
            d = d.dict(exclude_unset=True)
            query, values = generate_sql_insert(
                tenant_id=tenant_id,
                table=table_name,
                data=d,
            )
            query += " ON CONFLICT (id) DO UPDATE SET "
            query += ", ".join(
                f"{col} = EXCLUDED.{col}"
                for col in schema.model_fields.keys()
                if col != "id"
            )
            await db.execute(query, *values)

        return None
