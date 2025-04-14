from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID1, AwareDatetime

from app.core.auth.dependecies import (
    is_admin_and_tenant_info,
    is_trainer_and_tenant_info,
)
from app.core.auth.schemas import AuthData
from app.core.shared.database import get_db
from app.features.meet.disciplines.service import DisciplineService
from app.features.meet.schemas import (
    DisciplineCreatePublic,
    DisciplineReadPublic,
    DisciplineTypeCreatePublic,
    DisciplineTypeReadPublic,
    DisciplineUpdatePublic,
)

router = APIRouter(
    prefix="/discipline",
    tags=["discipline"],
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
        Depends(DisciplineService),
    ],
    default_response_class=ORJSONResponse,
)
trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
admin_dep = Annotated[AuthData, Depends(is_admin_and_tenant_info)]
db_dep = Annotated[Connection, Depends(get_db)]
service_dep = Annotated[DisciplineService, Depends(DisciplineService)]


@router.get(
    "/{discipline_id}",
    response_model=DisciplineReadPublic,
)
async def read_discipline(
    discipline_id: int,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> DisciplineReadPublic:
    discipline = await service.get_discipline_by_id(
        auth_data.tenant_id,
        discipline_id,
        db,
    )
    return ORJSONResponse(discipline, status_code=status.HTTP_200_OK)


@router.post(
    "/",
    response_model=DisciplineReadPublic,
)
async def create_discipline(
    discipline: DisciplineCreatePublic,
    auth_data: admin_dep,
    db: db_dep,
    service: service_dep,
) -> DisciplineReadPublic:
    discipline = await service.create_discipline(
        auth_data.tenant_id,
        discipline.model_dump(),
        db,
    )
    return ORJSONResponse(discipline, status_code=status.HTTP_201_CREATED)


@router.put(
    "/{discipline_id}",
    response_model=DisciplineReadPublic,
)
async def update_discipline(
    discipline_id: int,
    discipline: DisciplineUpdatePublic,
    auth_data: admin_dep,
    db: db_dep,
    service: service_dep,
) -> DisciplineReadPublic:
    if discipline_id != discipline.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discipline ID in path and body do not match",
        )
    discipline = await service.update_discipline(
        auth_data.tenant_id,
        discipline.model_dump(),
        db,
    )
    return ORJSONResponse(discipline, status_code=status.HTTP_200_OK)


@router.delete(
    "/{discipline_id}",
    response_model=DisciplineReadPublic,
)
async def delete_discipline(
    discipline_id: int,
    auth_data: admin_dep,
    db: db_dep,
    service: service_dep,
) -> DisciplineReadPublic:
    discipline = await service.delete_discipline(
        auth_data.tenant_id,
        discipline_id,
        db,
    )
    return ORJSONResponse(discipline, status_code=status.HTTP_200_OK)


@router.get(
    "/",
    response_model=list[DisciplineReadPublic],
)
async def read_all_disciplines(
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[DisciplineReadPublic]:
    disciplines = await service.get_all_disciplines(
        auth_data.tenant_id,
        db,
    )
    return ORJSONResponse(disciplines, status_code=status.HTTP_200_OK)


@router.get(
    "/type/",
    response_model=list[DisciplineTypeReadPublic],
)
async def read_all_discipline_types(
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[DisciplineTypeReadPublic]:
    discipline_types = await service.get_all_discipline_types(
        auth_data.tenant_id,
        db,
    )
    return ORJSONResponse(discipline_types, status_code=status.HTTP_200_OK)


@router.post(
    "/type/",
    response_model=DisciplineTypeReadPublic,
)
async def create_discipline_type(
    discipline_type: DisciplineTypeCreatePublic,
    auth_data: admin_dep,
    db: db_dep,
    service: service_dep,
) -> DisciplineTypeReadPublic:
    discipline_type = await service.create_discipline_type(
        auth_data.tenant_id,
        discipline_type.model_dump(),
        db,
    )
    return ORJSONResponse(discipline_type, status_code=status.HTTP_201_CREATED)
