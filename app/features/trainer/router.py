from datetime import datetime, timedelta
from typing import Annotated, Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from app.core.auth import admin_dep, trainer_dep
from app.core.database import get_tenant_db
from app.features.athlete.service import AthleteService
from app.models import Athlete, BaseModel, TrainingDashboardRead
from app.schemas.attendance import TrainingAttendanceDetail

from .service import TrainerService

router = APIRouter(
    prefix="/trainer",
    tags=["trainer"],
    responses={
        "200": {"description": "Success"},
        "400": {"description": "Bad Request"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
        "404": {"description": "Not Found"},
        "409": {"description": "Conflict"},
    },
    default_response_class=ORJSONResponse,
)
# db_dep = Annotated[AsyncSession, Depends(get_tenant_db)]
trainer_service_dep = Annotated[TrainerService, Depends(TrainerService)]


@router.get("/dashboard/schedule", response_model=List[TrainingDashboardRead])
async def get_dashboard_schedule(
    auth_data: trainer_dep,
    service: trainer_service_dep,
):
    now = datetime.now()
    end_date = now + timedelta(days=7)
    return await service.get_trainings_by_range(
        trainer_email=auth_data.email, start_date=now, end_date=end_date
    )


@router.get("/schedule/range", response_model=List[TrainingDashboardRead])
async def get_schedule_range(
    from_date: datetime,
    to_date: datetime,
    auth_data: trainer_dep,
    service: trainer_service_dep,
):
    return await service.get_trainings_by_range(
        trainer_email=auth_data.email, start_date=from_date, end_date=to_date
    )


# Define a small request body model for the update
class AttendanceUpdateRequest(BaseModel):
    description: str | None
    athlete_status: dict[UUID, str | None]  # Mapping of athlete_id to presence status
    trainer_status: dict[UUID, str | None]  # Mapping of trainer_id to presence status


@router.get("/attendance/{training_id}", response_model=TrainingAttendanceDetail)
async def get_attendance_detail(
    training_id: UUID,
    auth_data: trainer_dep,
    service: trainer_service_dep,
):
    return await service.get_attendance_detail(training_id)


@router.post("/attendance/{training_id}")
async def submit_attendance(
    training_id: UUID,
    payload: AttendanceUpdateRequest,
    auth_data: trainer_dep,
    service: trainer_service_dep,
):
    await service.update_attendance(
        training_id,
        payload.description,
        payload.athlete_status,
        payload.trainer_status,
    )
    return {"status": "success"}
