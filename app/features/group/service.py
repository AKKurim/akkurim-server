from uuid import UUID, uuid1

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
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
        if group_id:
            # UPDATE
            group = await self.db.get(Group, group_id)
            if not group:
                return None
            for key, value in data.model_dump(
                exclude={"trainer_ids", "athlete_ids"}
            ).items():
                setattr(group, key, value)

            # Clear old relations
            await self.db.exec(
                select(GroupTrainer).where(GroupTrainer.group_id == group_id).delete()
            )
            await self.db.exec(
                select(GroupAthlete).where(GroupAthlete.group_id == group_id).delete()
            )
        else:
            group = Group(**data.model_dump(exclude={"trainer_ids", "athlete_ids"}))
            self.db.add(group)
            await self.db.flush()  # Get ID

        # Insert new Relations
        for tid in data.trainer_ids:
            self.db.add(GroupTrainer(group_id=group.id, trainer_id=tid))

        for aid in data.athlete_ids:
            self.db.add(GroupAthlete(group_id=group.id, athlete_id=aid))

        await self.db.commit()
        await self.db.refresh(group)
        return group
