from asyncpg import Connection

from app.core.remote_config.schemas import RemoteConfigRead
from app.core.utils.default_service import DefaultService


class RemoteConfigService:
    def __init__(self) -> None:
        self.table: str = "remote_config"
        self.default_service: DefaultService = DefaultService(
            "remote_config",
            "/remote_config/{id}",
            RemoteConfigRead,
        )

    async def get_remote_config(
        self, tenant_id: str, db: Connection
    ) -> RemoteConfigRead:
        return await self.default_service.get_object_by_id(tenant_id, 0, db)
