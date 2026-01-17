import re
from datetime import datetime, timezone
from typing import Tuple

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

    def _convert_query_and_params(self, query: str, values: Tuple) -> Tuple[str, dict]:
        # convert $1, $2... placeholders to :p1, :p2... and build mapping
        if not values:
            return query, {}

        def repl(m):
            return f":p{m.group(1)}"

        new_query = re.sub(r"\$(\d+)", repl, query)
        params = {f"p{i+1}": v for i, v in enumerate(values)}
        return new_query, params

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
        sql, params = self._convert_query_and_params(query, (from_date,))
        result = await db.exec(text(sql), params=params)
        rows = result.all()
        return [r._mapping["table_name"] for r in rows]

    async def get_objects_to_sync(
        self,
        tenant_id: str,
        table_name: str,
        from_date: AwareDatetime,
        db: AsyncSession,
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
        sql, params = self._convert_query_and_params(query, tuple(values))
        result = await db.exec(text(sql), params=params)
        rows = result.all()
        return [convert_uuid_to_str(dict(r._mapping)) for r in rows]

    async def sync_objects(
        self,
        tenant_id: str,
        table_name: str,
        data: list[BaseModel],
        primary_keys: list[str],
        db: AsyncSession,
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
            sql, params = self._convert_query_and_params(query, values)
            await db.exec(text(sql), params=params)
            await db.commit()

        return None
