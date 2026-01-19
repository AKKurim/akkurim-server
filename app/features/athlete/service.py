from typing import List

from atletika_scraper import PrivateCASScraper
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.scraper import get_private_scraper
from app.models import Athlete, AthleteGuardian, File, Guardian


class AthleteService:
    def __init__(self):
        self.scraper: PrivateCASScraper = get_private_scraper()

    async def get_athlete_by_id(
        self,
        athlete_id: str,
        db: AsyncSession,
    ) -> Athlete | None:
        result = await db.get(Athlete, athlete_id)
        return result

    async def get_all_athletes(
        self,
        db: AsyncSession,
    ) -> List[Athlete]:
        result = await db.exec(select(Athlete))
        athletes = result.all()
        return athletes

    async def create_athlete(
        self,
        athlete: Athlete,
        db: AsyncSession,
    ) -> Athlete:
        db.add(athlete)
        await db.commit()
        await db.refresh(athlete)
        return athlete
