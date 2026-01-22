from broadcaster import Broadcast

from app.core.database import db_settings

broadcast = Broadcast(
    db_settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
)
