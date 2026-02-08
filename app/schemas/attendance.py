from uuid import UUID

from pydantic import BaseModel

from app.models.training import TrainingBase


class AthleteAttendanceItem(BaseModel):
    athlete_id: UUID
    first_name: str
    last_name: str
    presence: str | None  # e.g., "p - present", "a - absent", or excused reason


class TrainerAttendanceItem(BaseModel):
    trainer_id: UUID
    first_name: str
    last_name: str
    presence: str | None  # 'p', 'a', etc.


class TrainingAttendanceDetail(TrainingBase):
    id: UUID
    group_name: str
    athletes: list[AthleteAttendanceItem]
    trainers: list[TrainerAttendanceItem]
