# app/cron.py
import asyncio
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text
from sqlmodel import select

from app.core.database import sa_db  # your context manager
from app.core.notifications import notification_service
from app.models import Meet

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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
            await notification_service.send_notification_to_all(
                title="Blíží se začátek závodu!",
                message=f"{meet.name} začíná za méně než 24 hodin.",
            )
            print(f"Sent notification for meet {meet.id}", flush=True)


async def check_birthdays():
    """Runs once a day at 9:00 AM"""
    pass


# --- Scheduler Setup ---
scheduler = AsyncIOScheduler()

# Add jobs
scheduler.add_job(check_meet_starts, "cron", minute="*/15")  # for debug now
scheduler.add_job(check_birthdays, "cron", hour=9, minute=0)  # Run at 9:00 AM daily


async def main():
    logger.info("Starting Cron Worker...")
    scheduler.start()

    # Keep the script running
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    asyncio.run(main())
