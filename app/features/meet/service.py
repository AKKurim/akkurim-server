import uuid
from datetime import datetime, timezone
from typing import List

from atletika_scraper import PrivateCASScraper, PublicCASScraper
from atletika_scraper.schemas.athlete import AthleteRaceEntry
from atletika_scraper.schemas.meet import FullMeet
from atletika_scraper.schemas.meet_event import MeetEvent as ScraperMeetEvent
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
        db: AsyncSession,
        external_id: str,
        type: str,
    ) -> Meet | None:
        result = await db.execute(
            select(Meet).where(
                (Meet.external_id == external_id) & Meet.type.startswith(type)
            )
        )
        meet = result.scalars().one_or_none()
        return meet

    async def sync_meet_from_cas(
        self,
        db: AsyncSession,
        external_meet_id: str,
        type: str = "CAS",
        use_private_registrations: bool = False,
    ) -> Meet:
        reg_athletes = None
        if use_private_registrations:
            reg_athletes = self.private_scraper.get_registered_athletes_for_meet(
                external_meet_id
            )

        meet_data: FullMeet = self.public_scraper.get_full_meet_info(
            external_meet_id,
            reg_athletes=reg_athletes,
        )
        reg_start, reg_end = (
            self.private_scraper.get_meet_registrations_start_end_times(
                external_meet_id
            )
        )

        # find existing meet
        meet = await self._get_meet_by_external_id_type(db, external_meet_id, type)
        if meet is None:
            meet = Meet(
                id=str(uuid.uuid1()),
                external_id=external_meet_id,
                type=type,
                name=meet_data.name,
                start_at=meet_data.start.isoformat() + "+01:00",
                end_at=meet_data.end.isoformat() + "+01:00",
                registration_start_at=reg_start.isoformat() + "+01:00",
                registration_end_at=reg_end.isoformat() + "+01:00",
                location=meet_data.location,
                organizer=meet_data.organizer,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                last_updated_by="server",
            )
        else:
            meet.name = meet_data.name
            meet.start_at = meet_data.start.isoformat() + "+01:00"
            meet.end_at = meet_data.end.isoformat() + "+01:00"
            meet.registration_start_at = reg_start.isoformat() + "+01:00"
            meet.registration_end_at = reg_end.isoformat() + "+01:00"
            meet.location = meet_data.location
            meet.organizer = meet_data.organizer
            meet.updated_at = datetime.now(timezone.utc)
            meet.last_updated_by = "server"
        db.add(meet)
        await db.flush()

        # meet events
        # first try to select existing events
        existing_events_result = await db.execute(
            select(MeetEvent).where(MeetEvent.meet_id == meet.id)
        )
        existing_events: List[MeetEvent] = existing_events_result.scalars().all()

        for event in meet_data.meet_events:
            event: ScraperMeetEvent
            meet_event = next(
                (
                    e
                    for e in existing_events
                    if e.discipline_id == event.discipline_id
                    and e.category_id == event.category_id
                    and e.phase == event.phase
                ),
                None,
            )
            if meet_event is None:
                meet_event = MeetEvent(
                    id=str(uuid.uuid1()),
                    meet_id=meet.id,
                    discipline_id=event.discipline_id,
                    category_id=event.category_id,
                    phase=event.phase if event.phase is not None else "",
                    start_at=event.start.isoformat() + "+01:00",
                    count=None,  # TODO fill later
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                    last_updated_by="server",
                )
                existing_events.append(meet_event)
            else:
                meet_event.start_at = event.start.isoformat() + "+01:00"
                meet_event.updated_at = datetime.now(timezone.utc)
                meet_event.last_updated_by = "server"
            db.add(meet_event)
            await db.flush()
            for athlete_data in event.participants:
                athlete_data: AthleteRaceEntry
                athlete_result = await db.execute(
                    select(Athlete).where(
                        (Athlete.last_name == athlete_data.last_name)
                        & (Athlete.first_name == athlete_data.first_name)
                    )
                )
                athlete: Athlete = athlete_result.scalars().one_or_none()
                if athlete is None:
                    continue  # skip unregistered athletes
                # check if athlete already registered for the event
                athlete_meet_event_result = await db.execute(
                    select(AthleteMeetEvent).where(
                        (AthleteMeetEvent.athlete_id == athlete.id)
                        & (AthleteMeetEvent.meet_event_id == meet_event.id)
                    )
                )
                athlete_meet_event = athlete_meet_event_result.scalars().one_or_none()
                if athlete_meet_event is None:
                    athlete_meet_event = AthleteMeetEvent(
                        id=str(uuid.uuid1()),
                        athlete_id=athlete.id,
                        meet_event_id=meet_event.id,
                        bib=athlete_data.bib,
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc),
                        last_updated_by="server",
                    )
                    db.add(athlete_meet_event)
        await db.commit()
        return meet
