from datetime import datetime, timedelta
from typing import List

import sqlalchemy as sa
from fastapi import Depends
from sqlmodel import Session, and_, col, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_tenant_db

# Adjust these imports based on your actual file structure
from app.models import (
    Athlete,
    Group,
    GroupAthlete,
    GroupTrainer,
    Trainer,
    Training,
    TrainingAthlete,
    TrainingDashboardRead,
)


class TrainerService:
    def __init__(self, db: AsyncSession = Depends(get_tenant_db)):
        self.db: AsyncSession = db

    async def get_dashboard_schedule(
        self, trainer_email: str, days_ahead: int = 7
    ) -> List[TrainingDashboardRead]:

        # Time Window Logic (Start of Today -> +7 Days)
        now = datetime.now()
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now + timedelta(days=days_ahead)

        statement = (
            select(
                Training,
                Group.name.label("group_name"),
                sa.case(
                    (
                        Training.attendance_taken_at != None,
                        func.count(func.distinct(TrainingAthlete.athlete_id)),
                    ),
                    else_=func.count(func.distinct(GroupAthlete.athlete_id)),
                ).label("attendee_count"),
            )
            # --- THE NEW JOIN CHAIN ---
            .join(Group, Group.id == Training.group_id)
            .join(
                GroupTrainer, GroupTrainer.group_id == Group.id
            )  # Link Group -> Link Table
            .join(
                Trainer, Trainer.id == GroupTrainer.trainer_id
            )  # Link Table -> Trainer Profile
            .join(
                Athlete, Athlete.id == Trainer.athlete_id
            )  # Trainer Profile -> Athlete Profile
            # (If Athlete has a 'user_id' link to a User table, add one more join here.
            #  But assuming Athlete holds the email or links to it:)
            # --- AGGREGATION JOINS ---
            .outerjoin(GroupAthlete, GroupAthlete.group_id == Group.id)
            .outerjoin(TrainingAthlete, TrainingAthlete.training_id == Training.id)
            .where(
                and_(
                    # Filter by the Email found on the Athlete/User entity
                    Athlete.email == trainer_email,
                    Training.deleted_at == None,
                    Training.start_at >= start_of_today,
                    Training.start_at <= end_date,
                )
            )
            .group_by(Training.id, Group.name)
            .order_by(Training.start_at)
        )

        result = await self.db.exec(statement)
        rows = result.all()

        schedule_data = []
        for training, group_name, count in rows:
            schedule_data.append(
                TrainingDashboardRead(
                    **training.model_dump(), group_name=group_name, attendee_count=count
                )
            )

        return schedule_data
