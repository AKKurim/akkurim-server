from typing import Annotated, Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import AuthData, trainer_dep
from app.core.database import get_tenant_db
from app.models import Athlete

from .service import AthleteService

router = APIRouter(
    prefix="/athlete",
    tags=["athlete"],
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
db_dep = Annotated[AsyncSession, Depends(get_tenant_db)]
service_dep = Annotated[AthleteService, Depends(AthleteService)]


@router.get(
    "/{athlete_id}",
    response_model=Athlete,
)
async def get_athlete_by_id(
    athlete_id: UUID,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> Athlete:
    athlete = await service.get_athlete_by_id(athlete_id, db)
    return athlete


@router.post(
    "/",
    response_model=Athlete,
    status_code=status.HTTP_201_CREATED,
)
async def create_athlete(
    athlete: Athlete,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> Athlete:
    created_athlete = await service.create_athlete(athlete, db)
    return created_athlete
