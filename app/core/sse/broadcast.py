from broadcaster import Broadcast

from app.core.config import settings

broadcast = Broadcast(
    settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
)
