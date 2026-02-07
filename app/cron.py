# app/cron.py
import asyncio
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import sa_db  # your context manager
from app.core.logging import logger
from app.core.notifications import get_notification_service
from app.core.sse import broadcast
from app.features.meet.service import MeetService
from app.models import Meet

tenant = "kurim"


async def check_meet_starts():
    """Runs every 15 minutes for notifications"""
    # since new info is available precisely at :00, :15, :30, :45
    # we sleep for 1 second to ensure we are just past that time
    await asyncio.sleep(1)
    async_session = sa_db.get_sessionmaker()
    async with async_session() as session:
        now = datetime.utcnow()
        # select meets starting in the next 24 hours
        await session.execute(text("SET search_path TO " + tenant))
        upcoming_meets_results = await session.execute(
            select(Meet).where(
                Meet.start_at
                >= now + timedelta(hours=23, minutes=45),  # so it sent only once
                Meet.start_at < now + timedelta(hours=24),
            )
        )
        upcoming_meets = upcoming_meets_results.scalars().all()
        for meet in upcoming_meets:
            notification_service = get_notification_service()
            await notification_service.send_notification_to_all(
                title="Blíží se začátek závodu",
                message=f"{meet.name} začíná za 24 hodin.",
            )
            logger.info(f"Sent start notification for meet {meet.id}")


async def live_update_results():
    """Runs every 10 minutes during meets to update live results"""
    print("Running live update for results...")
    async_session = sa_db.get_sessionmaker()
    async with async_session() as session:
        session: AsyncSession
        await session.execute(text("SET search_path TO " + tenant))
        now = datetime.utcnow()
        ongoing_meets_results = await session.execute(
            select(Meet).where(
                Meet.start_at + timedelta(minutes=9) <= now,
                # buffer for first results since the event must happen
                Meet.end_at + timedelta(hours=3) >= now,
                # buffer for extended meets
            )
        )
        ongoing_meets = ongoing_meets_results.scalars().all()
        if len(ongoing_meets) == 0:
            logger.info("No ongoing meets for live update.")
            return
        meet_service = MeetService()
        for meet in ongoing_meets:
            meet: Meet
            await meet_service.sync_meet_results_from_cas(session, meet.external_id)
            logger.info(f"Updated live results for meet {meet.id}")
    print("Live update completed.")


async def check_birthdays():
    """Runs once a day at 9:00 AM"""
    pass


# --- Scheduler Setup ---
scheduler = AsyncIOScheduler()

# Add jobs
scheduler.add_job(check_meet_starts, "cron", minute="*/15")  # every 15 minutes
scheduler.add_job(live_update_results, "cron", minute="*/10")  # every 10 minutes
scheduler.add_job(check_birthdays, "cron", hour=9, minute=0)  # Run at 9:00 AM daily


async def main():
    logger.info("Starting Cron Worker...")
    await sa_db.connect()
    await broadcast.connect()
    scheduler.start()

    # Keep the script running
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown(wait=False)
        await broadcast.disconnect()
        await sa_db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
