from uuid import UUID

from app.models.training import TrainingBase


class TrainingDashboardRead(TrainingBase):
    id: UUID
    group_name: str
    attendee_count: int
