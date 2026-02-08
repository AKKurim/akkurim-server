from datetime import datetime, timezone
from uuid import UUID, uuid1

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from sqlmodel import update
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_tenant_db
from app.models import Athlete, Group, GroupAthlete, GroupTrainer, SchoolYear, Trainer
from app.schemas import GroupCreateUpdate, GroupDetailRead, PersonSimple


class GroupService:
    def __init__(self, db: AsyncSession = Depends(get_tenant_db)):
        self.db: AsyncSession = db

    async def get_all_school_years(self) -> list[SchoolYear]:
        stmt = select(SchoolYear).order_by(SchoolYear.name.desc())
        res = await self.db.exec(stmt)
        return res.scalars().all()

    async def get_all_people(self, role: str) -> list[PersonSimple]:
        """Helper to get all athletes or trainers for the dropdowns"""
        if role == "athlete":
            # Fetch simple athlete view
            stmt = (
                select(Athlete)
                .where(Athlete.status == "active")
                .where(Athlete.deleted_at == None)
                .order_by(Athlete.last_name)
            )
            res = await self.db.exec(stmt)
            all_athletes = res.scalars().all()
            print(all_athletes)
            return [
                PersonSimple(id=a.id, first_name=a.first_name, last_name=a.last_name)
                for a in all_athletes
            ]

        elif role == "trainer":
            stmt = (
                select(Trainer, Athlete).join(Athlete).where(Trainer.deleted_at == None)
            )
            res = await self.db.exec(stmt)
            return [
                PersonSimple(id=t.id, first_name=a.first_name, last_name=a.last_name)
                for t, a in res.all()
            ]

    async def get_group_details(self, group_id: UUID) -> GroupDetailRead:
        # Fetch Group with relations
        stmt = select(Group).where(Group.id == group_id)
        result = await self.db.exec(stmt)
        group: Group = result.scalar_one_or_none()
        if not group:
            return None

        # Fetch related trainers and athletes
        trainers_stmt = (
            select(Trainer, Athlete)
            .join(GroupTrainer, GroupTrainer.trainer_id == Trainer.id)
            .join(Athlete, Athlete.id == Trainer.athlete_id)
            .where(GroupTrainer.group_id == group_id)
            .where(GroupTrainer.deleted_at == None)
            .where(Trainer.deleted_at == None)
            .where(Athlete.deleted_at == None)
            .order_by(Athlete.last_name)
        )
        trainers_res = await self.db.exec(trainers_stmt)
        trainers = [
            PersonSimple(id=t.id, first_name=a.first_name, last_name=a.last_name)
            for t, a in trainers_res.all()
        ]
        athletes_stmt = (
            select(Athlete)
            .join(GroupAthlete, GroupAthlete.athlete_id == Athlete.id)
            .where(GroupAthlete.group_id == group_id)
            .where(GroupAthlete.deleted_at == None)
            .where(Athlete.deleted_at == None)
            .order_by(Athlete.last_name)
        )
        athletes_res = await self.db.exec(athletes_stmt)
        athletes = [
            PersonSimple(id=a.id, first_name=a.first_name, last_name=a.last_name)
            for a in athletes_res.scalars().all()
        ]
        group_detail = GroupDetailRead(
            **group.model_dump(exclude={"created_at", "updated_at", "deleted_at"}),
            trainers=trainers,
            athletes=athletes,
        )

        return group_detail

    async def upsert_group(
        self, data: GroupCreateUpdate, group_id: UUID = None
    ) -> Group:
        now_ts = datetime.now(timezone.utc)

        if group_id:
            # UPDATE
            group = await self.db.get(Group, group_id)
            if not group:
                return None
            for key, value in data.model_dump(
                exclude={"trainer_ids", "athlete_ids"}
            ).items():
                setattr(group, key, value)
            group.updated_at = now_ts

            # Soft-delete previous relations by setting timestamps
            await self.db.exec(
                update(GroupTrainer)
                .where(GroupTrainer.group_id == group_id)
                .values(updated_at=now_ts, deleted_at=now_ts)
            )
            await self.db.exec(
                update(GroupAthlete)
                .where(GroupAthlete.group_id == group_id)
                .values(updated_at=now_ts, deleted_at=now_ts)
            )
        else:
            group = Group(**data.model_dump(exclude={"trainer_ids", "athlete_ids"}))
            group.updated_at = now_ts
            self.db.add(group)
            await self.db.flush()  # Get ID

        # Insert new Relations
        for tid in data.trainer_ids:
            # check if relation already exists and is soft-deleted; if so, just reset timestamps instead of inserting new
            existing_trainer_rel = await self.db.exec(
                select(GroupTrainer).where(
                    (GroupTrainer.group_id == group.id)
                    & (GroupTrainer.trainer_id == tid)
                )
            )
            existing_trainer_rel = existing_trainer_rel.scalar_one_or_none()
            if existing_trainer_rel:
                existing_trainer_rel.updated_at = now_ts
                existing_trainer_rel.deleted_at = (
                    None  # "undelete" if it was soft-deleted
                )
            else:
                self.db.add(
                    GroupTrainer(
                        group_id=group.id,
                        trainer_id=tid,
                        created_at=now_ts,
                        updated_at=now_ts,
                    )
                )

        for aid in data.athlete_ids:
            existing_athlete_rel = await self.db.exec(
                select(GroupAthlete).where(
                    (GroupAthlete.group_id == group.id)
                    & (GroupAthlete.athlete_id == aid)
                )
            )
            existing_athlete_rel = existing_athlete_rel.scalar_one_or_none()
            if existing_athlete_rel:
                existing_athlete_rel.updated_at = now_ts
                existing_athlete_rel.deleted_at = None
            else:
                self.db.add(
                    GroupAthlete(
                        group_id=group.id,
                        athlete_id=aid,
                        created_at=now_ts,
                        updated_at=now_ts,
                    )
                )

        # Do not commit or refresh here — the tenant DB dependency
        # manages the transaction for the request. Committing here
        # would close the transaction context and cause errors.
        return group
