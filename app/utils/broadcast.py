from broadcaster import Broadcast

from app.config import settings

broadcast = Broadcast(settings.DATABASE_URL)
