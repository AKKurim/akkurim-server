from uuid import UUID

import sqlalchemy as sa
from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel

from ._base_model import BaseModel


class AthleteRegistrationMeetEvent(BaseModel, table=True):
    __tablename__ = "athlete_registration_meet_event"

    athlete_id: UUID = Field(primary_key=True, foreign_key="athlete.id", index=True)
    meet_event_id: UUID = Field(
        primary_key=True, foreign_key="meet_event.id", index=True
    )
    status: str = Field(nullable=False)
