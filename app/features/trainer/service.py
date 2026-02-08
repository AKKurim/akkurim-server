from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID

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
)
from app.models.training_trainer import TrainingTrainer
from app.schemas import TrainingDashboardRead
from app.schemas.attendance import (
    AthleteAttendanceItem,
    TrainerAttendanceItem,
    TrainingAttendanceDetail,
)


class TrainerService:
    def __init__(self, db: AsyncSession = Depends(get_tenant_db)):
        self.db: AsyncSession = db

    async def get_trainings_by_range(
        self, trainer_email: str, start_date: datetime, end_date: datetime
    ) -> List[TrainingDashboardRead]:

        # Time Window Logic (Start of Today -> +7 Days)
        now = datetime.now()
        start_of_start_date = datetime(
            year=start_date.year, month=start_date.month, day=start_date.day
        )

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
                    Training.start_at >= start_of_start_date,
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

    async def get_attendance_detail(
        self, training_id: UUID
    ) -> TrainingAttendanceDetail:
        # 1. FETCH TRAINING & GROUP
        #    We need to select 'Training' into a variable so we can use .model_dump() later
        query_training = (
            select(Training, Group.name)
            .join(Group, Group.id == Training.group_id)
            .where(Training.id == training_id)
        )
        res_training = await self.db.exec(query_training)
        row = res_training.first()

        if not row:
            # Handle 404 case (or return None and handle in router)
            return None

        # --- THIS DEFINES THE VARIABLE ---
        training, group_name = row

        # 2. ATHLETES: Fetch Status String directly
        #    Join GroupAthlete to get everyone in the group.
        #    Outer Join AthleteTraining to get their status if it exists.
        query_athletes = (
            select(
                Athlete.id,
                Athlete.first_name,
                Athlete.last_name,
                TrainingAthlete.presence,  # Fetch 'p', 'a', 'e', 'sick', or None
            )
            .join(GroupAthlete, GroupAthlete.athlete_id == Athlete.id)
            .outerjoin(
                TrainingAthlete,
                and_(
                    TrainingAthlete.athlete_id == Athlete.id,
                    TrainingAthlete.training_id == training_id,
                ),
            )
            .where(GroupAthlete.group_id == training.group_id)
            .order_by(Athlete.last_name, Athlete.first_name)
        )
        res_athletes = await self.db.exec(query_athletes)
        athletes = res_athletes.all()

        # 3. TRAINERS: Fetch Trainer Attendance
        #    Fetch trainers assigned to this group + their status for this specific training.
        query_trainers = (
            select(
                Trainer.id,
                Athlete.first_name,
                Athlete.last_name,
                TrainingTrainer.presence,
            )
            .join(GroupTrainer, GroupTrainer.trainer_id == Trainer.id)
            # Assuming Trainer -> User link for names. Adjust if your Trainer model has name fields directly.
            .join(Athlete, Athlete.id == Trainer.athlete_id)
            .outerjoin(
                TrainingTrainer,
                and_(
                    TrainingTrainer.trainer_id == Trainer.id,
                    TrainingTrainer.training_id == training_id,
                ),
            )
            .where(GroupTrainer.group_id == training.group_id)
        )
        res_trainers = await self.db.exec(query_trainers)
        trainers = res_trainers.all()
        print("Trainers Attendance Query Result:", trainers, flush=True)

        # 4. CONSTRUCT RESPONSE
        return TrainingAttendanceDetail(
            **training.model_dump(),  # Now 'training' is safely defined from Step 1
            group_name=group_name,
            athletes=[
                AthleteAttendanceItem(
                    athlete_id=a_id,
                    first_name=fname,
                    last_name=lname,
                    # If presence is None (no record), default to 'a' (Absent)
                    # OR keep as None if you want the UI to show "Unmarked" state
                    presence=presence,
                )
                for a_id, fname, lname, presence in athletes
            ],
            trainers=[
                TrainerAttendanceItem(
                    trainer_id=t_id,
                    first_name=fname,
                    last_name=lname,
                    presence=presence,
                )
                for t_id, fname, lname, presence in trainers
            ],
        )

    async def update_attendance(
        self,
        training_id: UUID,
        description: str | None,
        # Map of ID -> Status String
        athlete_status: dict[UUID, str],
        trainer_status: dict[UUID, str],
    ):
        # 1. Update Training Metadata
        training = await self.db.get(Training, training_id)
        if training:
            training.description = description
            training.attendance_taken_at = datetime.now(timezone.utc)
            training.updated_at = datetime.now(timezone.utc)
            self.db.add(training)

        # 2. Update ATHLETES
        #    Delete old, insert new (simpler than upsert for bulk)
        await self.db.exec(
            sa.delete(TrainingAthlete).where(TrainingAthlete.training_id == training_id)
        )

        for ath_id, status in athlete_status.items():
            self.db.add(
                TrainingAthlete(
                    training_id=training_id,
                    athlete_id=ath_id,
                    presence=status,  # Store 'p', 'a', 'e', or 'flu'
                )
            )

        # 3. Update TRAINERS
        await self.db.exec(
            sa.delete(TrainingTrainer).where(TrainingTrainer.training_id == training_id)
        )

        for tr_id, status in trainer_status.items():
            self.db.add(
                TrainingTrainer(
                    training_id=training_id, trainer_id=tr_id, presence=status
                )
            )

        await self.db.commit()
