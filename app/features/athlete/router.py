from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID1, AwareDatetime
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.auth.dependecies import is_trainer_and_tenant_info
from app.core.auth.schemas import AuthData
from app.core.database import get_db
from app.features.athlete.schemas import (
    AthleteCreatePublic,
    AthleteReadPublic,
    AthleteUpdatePublic,
)
from app.features.athlete.service import AthleteService

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
    dependencies=[
        Depends(get_db),
        Depends(AthleteService),
    ],
    default_response_class=ORJSONResponse,
)

trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
db_dep = Annotated[Connection, Depends(get_db)]
service_dep = Annotated[AthleteService, Depends(AthleteService)]


@router.get(
    "/{athlete_id}",
    response_model=AthleteReadPublic,
)
async def read_athlete(
    athlete_id: UUID1,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> AthleteReadPublic:
    athlete = await service.get_athlete_by_id(
        auth_data.tenant_id,
        athlete_id,
        db,
    )
    return ORJSONResponse(athlete, status_code=status.HTTP_200_OK)


@router.post(
    "/",
    response_model=AthleteReadPublic,
)
async def create_athlete(
    athlete: AthleteCreatePublic,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> AthleteReadPublic:
    created_athlete = await service.create_athlete(
        auth_data.tenant_id,
        athlete.model_dump(),
        db,
    )
    return ORJSONResponse(created_athlete, status_code=status.HTTP_201_CREATED)


@router.put(
    "/{athlete_id}",
    response_model=AthleteReadPublic,
)
async def update_athlete(
    athlete_id: UUID1,
    athlete: AthleteUpdatePublic,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> AthleteReadPublic:
    updated_athlete = await service.update_athlete(
        auth_data.tenant_id,
        athlete_id,
        athlete.model_dump(),
        db,
    )
    return ORJSONResponse(updated_athlete, status_code=status.HTTP_200_OK)


@router.delete(
    "/{athlete_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_athlete(
    athlete_id: UUID1,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> None:
    await service.delete_athlete(
        auth_data.tenant_id,
        athlete_id,
        db,
    )
    return ORJSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/",
    response_model=list[AthleteReadPublic],
)
async def read_athletes(
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[AthleteReadPublic]:
    athletes = await service.get_all_athletes(
        auth_data.tenant_id,
        db,
    )
    return ORJSONResponse(athletes, status_code=status.HTTP_200_OK)


@router.get(
    "/sync/",
    response_model=list[AthleteReadPublic],
)
async def read_athletes_updated_after(
    last_updated_at: AwareDatetime,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[AthleteReadPublic]:
    athletes = await service.get_all_athletes_updated_after(
        auth_data.tenant_id,
        last_updated_at,
        db,
    )
    return ORJSONResponse(athletes, status_code=status.HTTP_200_OK)
