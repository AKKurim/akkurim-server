import uuid
from datetime import datetime, timezone
from typing import Annotated, List

import orjson
from atletika_scraper import PrivateCASScraper, PublicCASScraper
from atletika_scraper.pdf import create_pdf_schedule, create_pdf_schedule_athlete_cards
from atletika_scraper.schemas.athlete import AthleteRaceEntry
from atletika_scraper.schemas.discipline import get_discipline_by_id
from atletika_scraper.schemas.meet import FullMeet
from atletika_scraper.schemas.meet_event import MeetEvent as ScraperMeetEvent
from fastapi import Depends
from pydantic import UUID1
from sqlalchemy import text
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import AuthData
from app.core.exceptions import NotFoundError
from app.core.notifications import get_notification_service
from app.core.notifications.service import NotificationService
from app.core.scraper import get_private_scraper, get_public_scraper
from app.core.sse.broadcast import broadcast
from app.core.sse.schemas import LocalActionEnum, SSEEvent
from app.models import Athlete, AthleteMeetEvent, Discipline, Meet, MeetEvent, Trainer


class MeetService:
    def __init__(
        self,
        notification_service: NotificationService = Depends(get_notification_service),
    ):
        self.private_scraper: PrivateCASScraper = get_private_scraper()
        self.public_scraper: PublicCASScraper = get_public_scraper()
        self.club_filter = "Kuřim"
        self.broadcast = broadcast
        self.broadcast_endpoint = "/meet"
        self.table = "meet"
        self.notification_service = notification_service

    async def notify_update(self, tenant: str, id: UUID1) -> None:
        event = SSEEvent(
            tenant=tenant,
            table_name=self.table,
            endpoint=self.broadcast_endpoint,
            id=str(id),
            local_action=LocalActionEnum.upsert,
        )
        await self.broadcast.publish(
            channel="update",
            message=orjson.dumps(event.model_dump()).decode("utf-8"),
        )

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

    async def get_meet_by_external_id_type(
        self,
        external_id: str,
        type: str,
        db: AsyncSession,
    ) -> Meet:
        meet = await self._get_meet_by_external_id_type(db, external_id, type)
        if meet is None:
            raise NotFoundError("Meet not found")
        return meet

    async def get_meet_events_by_meet_id(
        self,
        meet_id: str,
        db: AsyncSession,
    ) -> List[MeetEvent]:
        result = await db.execute(select(MeetEvent).where(MeetEvent.meet_id == meet_id))
        meet_events = result.scalars().all()
        return meet_events

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
            club_filter=self.club_filter,
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
                        bib=str(athlete_data.bib),
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc),
                        last_updated_by="server",
                    )
                    db.add(athlete_meet_event)
        await db.commit()
        await self.notify_update("kurim", meet.id)
        return meet

    async def sync_meet_results_from_cas(
        self,
        db: AsyncSession,
        external_meet_id: str,
        type: str = "CAS",
    ) -> None:
        meet_results_data = self.public_scraper.get_athlete_results(
            external_meet_id,
            club_filter=self.club_filter,
        )
        meet_res = await db.execute(
            select(Meet).where(
                (Meet.external_id == external_meet_id) & Meet.type.startswith(type)
            )
        )
        meet: Meet = meet_res.scalars().one_or_none()
        if meet is None:
            raise NotFoundError(external_meet_id, "Meet not found")

        for athlete_result in meet_results_data:
            # try to find existing meet_event
            athlete_result: AthleteRaceEntry
            meet_event_result = await db.execute(
                select(MeetEvent).where(
                    (MeetEvent.meet_id == meet.id)
                    & (MeetEvent.discipline_id == athlete_result.discipline_id)
                    & (MeetEvent.category_id == athlete_result.category_id)
                    & (MeetEvent.phase == athlete_result.phase)
                )
            )
            meet_event: MeetEvent = meet_event_result.scalars().one_or_none()
            if meet_event is None:
                # try to find an event without finale phase
                finale_text = "Finále"
                meet_event_result = await db.execute(
                    select(MeetEvent).where(
                        (MeetEvent.meet_id == meet.id)
                        & (MeetEvent.discipline_id == athlete_result.discipline_id)
                        & (MeetEvent.category_id == athlete_result.category_id)
                        & (MeetEvent.phase != finale_text)
                    )
                )
                meet_event = meet_event_result.scalars().one_or_none()
            if meet_event is None:
                meet = await self.get_meet_by_external_id_type(
                    external_meet_id,
                    type,
                    db,
                )
                # create new meet event
                meet_event = MeetEvent(
                    id=str(uuid.uuid1()),
                    meet_id=meet.id,
                    discipline_id=athlete_result.discipline_id,
                    category_id=athlete_result.category_id,
                    start_at=(
                        athlete_result.start.isoformat() + "+01:00"
                        if athlete_result.start
                        else None
                    ),  # unknown
                    phase=athlete_result.phase,
                    count=None,  # TODO fill later
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                    last_updated_by="server",
                )
                db.add(meet_event)
                await db.flush()

            athletes: List[Athlete] = []
            # find athlete
            if athlete_result.is_relay_name:
                last_names = map(str.strip, athlete_result.last_name.split(","))
                athletes_result = await db.execute(
                    select(Athlete).where(Athlete.last_name.in_(last_names))
                )
                # if there is two results with same last name, look into all
                # athletes in meet_results_data to check if the athlete took
                # any other discipline (non-relay) to identify them correctly
                unparsed_athletes: List[Athlete] = athletes_result.scalars().all()
                for unparsed_athlete in unparsed_athletes:
                    found = next(
                        (
                            other_result
                            for other_result in meet_results_data
                            if (unparsed_athlete.first_name == other_result.first_name)
                            and (unparsed_athlete.last_name == other_result.last_name)
                            and not other_result.is_relay_name
                        ),
                        None,
                    )
                    if found is not None:
                        athletes.append(unparsed_athlete)
            else:
                athlete_result_db = await db.execute(
                    select(Athlete).where(
                        (Athlete.last_name == athlete_result.last_name)
                        & (Athlete.first_name == athlete_result.first_name)
                    )
                )
                athlete_db: Athlete = athlete_result_db.scalars().one_or_none()
                if athlete_db:
                    athletes.append(athlete_db)
            for athlete in athletes:
                parsed_points = (
                    str(int(athlete_result.points))
                    if athlete_result.points
                    and athlete_result.points == int(athlete_result.points)
                    else str(athlete_result.points) if athlete_result.points else None
                )
                # find athlete meet event
                athlete_meet_event_result = await db.execute(
                    select(AthleteMeetEvent).where(
                        (AthleteMeetEvent.athlete_id == athlete.id)
                        & (AthleteMeetEvent.meet_event_id == meet_event.id)
                    )
                )
                athlete_meet_event: AthleteMeetEvent = (
                    athlete_meet_event_result.scalars().one_or_none()
                )
                previous_result = (
                    athlete_meet_event.result if athlete_meet_event else None
                )
                if athlete_meet_event is None:
                    athlete_meet_event = AthleteMeetEvent(
                        athlete_id=athlete.id,
                        meet_event_id=meet_event.id,
                        result=athlete_result.result,
                        wind=athlete_result.wind,
                        pb_sb=athlete_result.pb_sb,
                        points=parsed_points,
                        bib=str(athlete_result.bib),
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc),
                        last_updated_by="server",
                    )
                else:
                    athlete_meet_event.result = athlete_result.result
                    athlete_meet_event.wind = athlete_result.wind
                    athlete_meet_event.pb_sb = athlete_result.pb_sb
                    athlete_meet_event.points = parsed_points
                    athlete_meet_event.updated_at = datetime.now(timezone.utc)
                    athlete_meet_event.last_updated_by = "server"
                db.add(athlete_meet_event)

                # actually send notification if the value changed
                if previous_result != athlete_meet_event.result:
                    self.notification_service.send_notification_to_all(
                        title="Nový výsledek závodu",
                        message=(
                            f"{athlete.first_name} {athlete.last_name} - "
                            f"{get_discipline_by_id(meet_event.discipline_id).short_description} - "
                            f"{athlete_meet_event.result} {'(' + athlete_meet_event.wind + ')' if athlete_meet_event.wind else ''} "
                            f"{athlete_meet_event.pb_sb if athlete_meet_event.pb_sb else ''} "
                        ),
                    )
        await db.commit()
        await self.notify_update("kurim", meet.id)
        return meet
