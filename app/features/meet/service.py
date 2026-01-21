import uuid
from datetime import datetime, timezone
from typing import List

from atletika_scraper import PrivateCASScraper, PublicCASScraper
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import AuthData
from app.core.exceptions import NotFoundError
from app.core.scraper import get_private_scraper, get_public_scraper
from app.models import Athlete, AthleteMeetEvent, Meet, MeetEvent, Trainer


class MeetService:
    def __init__(self):
        self.private_scraper: PrivateCASScraper = get_private_scraper()
        self.public_scraper: PublicCASScraper = get_public_scraper()

    async def get_meet_by_id(
        self,
        meet_id: str,
        db: AsyncSession,
    ) -> Meet:
        result = await db.get(Meet, meet_id)
        if result is None:
            raise NotFoundError("Meet not found")
        return result

    async def _get_meet_by_external_id_type(
        self,
        external_id: str,
        type: str,
        db: AsyncSession,
    ) -> Meet | None:
        result = await db.execute(
            select(Meet).where(
                Meet.external_id == external_id & Meet.type.startswith(type)
            )
        )
        meet = result.scalars().one_or_none()
        return meet
