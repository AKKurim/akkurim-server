import uuid
from datetime import datetime, timezone
from typing import List

from atletika_scraper import PrivateCASScraper
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import AuthData
from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.core.scraper import get_private_scraper
from app.models import Athlete, AthleteGuardian, File, Guardian, Trainer

from .config import athlete_settings


class AthleteService:
    def __init__(self):
        self.scraper: PrivateCASScraper = get_private_scraper()

    async def get_athlete_by_id(
        self,
        athlete_id: str,
        db: AsyncSession,
    ) -> Athlete:
        result = await db.get(Athlete, athlete_id)
        if result is None:
            raise NotFoundError("Athlete not found")
        return result

    async def _get_athlete_by_ean(
        self,
        ean: str,
        db: AsyncSession,
    ) -> Athlete | None:
        result = await db.execute(select(Athlete).where(Athlete.ean == ean))
        athlete = result.scalars().one_or_none()
        return athlete

    async def _get_trainer_by_athlete_id(
        self,
        athlete_id: str,
        db: AsyncSession,
    ) -> Trainer | None:
        result = await db.execute(
            select(Trainer).where(Trainer.athlete_id == athlete_id)
        )
        trainer = result.scalars().one_or_none()
        return trainer

    # admin function to sync athletes from CAS
    async def sync_athletes_from_cas(
        self,
        db: AsyncSession,
        auth_data: AuthData,
    ) -> List[Athlete]:
        data = self.scraper._get_all_members_data()
        athletes_data, count = data["data"], data["total"]
        for a_data in athletes_data:
            if a_data["JeAtlet"] == False and (
                a_data["DtTrenerPlatnostDo"] is None
                or a_data["DtTrenerPlatnostDo"] < datetime.now().isoformat()
            ):
                continue

            # athletes
            athlete = await self._get_athlete_by_ean(
                str(a_data["Ean"]),
                db,
            )
            if athlete is None:
                athlete = Athlete(
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                    last_updated_by="server",
                    id=str(uuid.uuid1()),
                    bank_number=None,
                    birth_number=a_data["RodneCislo"],
                    first_name=a_data["Jmeno"],
                    last_name=a_data["Prijmeni"],
                    street=a_data["AdresaUliceCp"],
                    city=a_data["AdresaMesto"],
                    zip=a_data["AdresaPsc"],
                    email=a_data["Email"],
                    phone=a_data["Telefon"],
                    ean=str(a_data["Ean"]),
                    note=None,
                    club_id=auth_data.tenant_id,
                    profile_image_id=None,
                    status="active",
                )
            else:
                athlete.updated_at = datetime.now(timezone.utc)
                athlete.first_name = a_data["Jmeno"]
                athlete.last_name = a_data["Prijmeni"]
                athlete.street = a_data["AdresaUliceCp"]
                athlete.city = a_data["AdresaMesto"]
                athlete.zip = a_data["AdresaPsc"]
                athlete.email = a_data["Email"]
                athlete.phone = a_data["Telefon"]
            db.add(athlete)

            # trainers
            if a_data["TrenerTrida"] != 0:
                trainer = await self._get_trainer_by_athlete_id(
                    athlete.id,
                    db,
                )
                if trainer is None:
                    trainer = Trainer(
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc),
                        last_updated_by="server",
                        id=str(uuid.uuid1()),
                        athlete_id=athlete.id,
                        qualification=athlete_settings.TRAINER_QUALIFICATION_MAPPING.get(
                            a_data["TrenerTrida"],
                            "Neznámá kvalifikace",
                        ),
                        bank_number=None,
                        status="active",
                        salary_per_hour=150,
                    )
                else:
                    trainer.updated_at = datetime.now(timezone.utc)
                    trainer.qualification = (
                        athlete_settings.TRAINER_QUALIFICATION_MAPPING.get(
                            a_data["TrenerTrida"],
                            "Neznámá kvalifikace",
                        )
                    )
                db.add(trainer)

            # guardians
            if (
                a_data["EmailZastupce"] is not None
                or a_data["TelefonZastupce"] is not None
            ):
                result = await db.execute(
                    select(Guardian).where((Guardian.email == a_data["EmailZastupce"]))
                )
                guardian = result.scalars().one_or_none()
                if guardian is None:
                    guardian = Guardian(
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc),
                        last_updated_by="server",
                        id=str(uuid.uuid1()),
                        first_name="Neznámé jméno",
                        last_name="Neznámé příjmení",
                        email=a_data["EmailZastupce"],
                        phone=a_data["TelefonZastupce"],
                    )
                    db.add(guardian)
                    await db.flush()  # to get guardian.id

                # link athlete and guardian
                result = await db.execute(
                    select(AthleteGuardian).where(
                        (AthleteGuardian.athlete_id == athlete.id)
                        & (AthleteGuardian.guardian_id == guardian.id)
                    )
                )
                athlete_guardian = result.scalars().one_or_none()
                if athlete_guardian is None:
                    athlete_guardian = AthleteGuardian(
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc),
                        last_updated_by="server",
                        athlete_id=athlete.id,
                        guardian_id=guardian.id,
                    )
                    db.add(athlete_guardian)

        await db.commit()
        athletes = await self.get_all_athletes(db)
        return athletes

        # todo sync also guardians and trainers

    async def get_all_athletes(
        self,
        db: AsyncSession,
    ) -> List[Athlete]:
        result = await db.execute(select(Athlete).where(Athlete.deleted_at == None))
        athletes = result.scalars().all()
        return athletes

    async def create_athlete(
        self,
        athlete: Athlete,
        db: AsyncSession,
    ) -> Athlete:
        try:
            db.add(athlete)
            await db.commit()
            await db.refresh(athlete)
            return athlete
        # if the athlete already exists return
        except Exception as e:
            await db.rollback()
            raise e

    async def delete_athlete(
        self,
        athlete_id: str,
        db: AsyncSession,
    ) -> None:
        athlete = await self.get_athlete_by_id(athlete_id, db)
        # set deleted_at timestamp
        athlete.deleted_at = datetime.now(timezone.utc)
        db.add(athlete)
        await db.commit()
