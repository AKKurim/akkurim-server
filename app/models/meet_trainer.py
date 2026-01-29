from uuid import UUID

from sqlmodel import Field

from ._base_model import BaseModel


class MeetTrainer(BaseModel, table=True):
    __tablename__ = "meet_trainer"

    meet_id: UUID = Field(primary_key=True, foreign_key="meet.id", index=True)
    trainer_id: UUID = Field(primary_key=True, foreign_key="trainer.id", index=True)
    status: str | None = Field(default=None)
    presence: str | None = Field(default=None)
