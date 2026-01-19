from typing import List

from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Athlete, AthleteGuardian, File, Guardian


class AthleteService:
    def __init__(self):
        pass

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
