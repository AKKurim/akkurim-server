from datetime import datetime
from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID1

from app.core.auth.dependecies import (
    is_trainer_and_tenant_info,
    verify_and_get_auth_data,
)
from app.core.auth.schemas import AuthData
from app.core.database import get_db
from app.features.guardian.schemas import GuardianCreate, GuardianRead, GuardianUpdate
from app.features.guardian.service import GuardianService

router = APIRouter(
    prefix="/guardian",
    tags=["guardian"],
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
        Depends(GuardianService),
    ],
    default_response_class=ORJSONResponse,
)

trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
db_dep = Annotated[Connection, Depends(get_db)]
service_dep = Annotated[GuardianService, Depends(GuardianService)]


@router.get(
    "/{guardian_id}",
    response_model=GuardianRead,
)
async def read_guardian(
    guardian_id: UUID1,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> GuardianRead:
    guardian = await service.get_guardian_by_id(
        auth_data.tenant_id,
        guardian_id,
        db,
    )
    return ORJSONResponse(guardian, status_code=status.HTTP_200_OK)


@router.post(
    "/",
    response_model=GuardianRead,
    responses={status.HTTP_201_CREATED: {"description": "Created"}},
)
async def create_guardian(
    guardian: GuardianCreate,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> GuardianRead:
    guardian = await service.create_guardian(
        auth_data.tenant_id,
        guardian.model_dump(),
        db,
    )
    return ORJSONResponse(guardian, status_code=status.HTTP_201_CREATED)


@router.put(
    "/{guardian_id}",
    response_model=GuardianRead,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
)
async def update_guardian(
    guardian_id: UUID1,
    guardian: GuardianUpdate,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> GuardianRead:
    if guardian_id != guardian.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Guardian ID in URL and body does not match",
        )
    guardian = await service.update_guardian(
        auth_data.tenant_id,
        guardian.model_dump(),
        db,
    )
    return ORJSONResponse(guardian, status_code=status.HTTP_200_OK)


@router.delete(
    "/{guardian_id}",
    status_code=204,
    response_model=None,
    responses={status.HTTP_204_NO_CONTENT: {"description": "Deleted"}},
)
async def delete_guardian(
    guardian_id: UUID1,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> ORJSONResponse:
    await service.delete_guardian(
        auth_data.tenant_id,
        guardian_id,
        db,
    )
    return ORJSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/",
    response_model=list[GuardianRead],
)
async def read_all_guardians(
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[dict]:
    guardians = await service.get_all_guardians(
        auth_data.tenant_id,
        db,
    )
    return ORJSONResponse(guardians, status_code=status.HTTP_200_OK)


# todo probably move the updated_at to query params
@router.get(
    "/sync/{last_updated_at}",
    response_model=list[GuardianRead],
)
async def read_all_guardians_updated_after(
    last_updated_at: Annotated[datetime, Path(...)],
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[dict]:
    guardians = await service.get_all_guardians_updated_after(
        auth_data.tenant_id,
        last_updated_at,
        db,
    )
    return ORJSONResponse(guardians, content={}, status_code=status.HTTP_200_OK)
