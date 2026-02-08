from typing import Annotated, Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.core.auth import admin_dep, trainer_dep
from app.models import Athlete, Group, SchoolYear
from app.schemas.group import GroupCreateUpdate, GroupDetailRead, PersonSimple

from .service import GroupService

router = APIRouter(
    prefix="/group",
    tags=["group"],
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
group_service_dep = Annotated[GroupService, Depends(GroupService)]


@router.get(
    "/school-years",
    response_model=List[SchoolYear],  # Adjust this to your actual SchoolYear schema
)
async def get_all_school_years(
    auth_data: trainer_dep,
    service: group_service_dep,
):
    return await service.get_all_school_years()


@router.get(
    "/athletes/all",
    response_model=List[PersonSimple],
)
async def get_all_athletes(
    auth_data: trainer_dep,
    service: group_service_dep,
):
    return await service.get_all_people("athlete")


@router.get(
    "/trainers/all",
    response_model=List[PersonSimple],
)
async def get_all_trainers(
    auth_data: trainer_dep,
    service: group_service_dep,
):
    return await service.get_all_people("trainer")


@router.get(
    "/{group_id}",
    response_model=GroupDetailRead,
)
async def get_group(
    group_id: UUID,
    auth_data: trainer_dep,
    service: group_service_dep,
) -> GroupDetailRead:
    group = await service.get_group_details(group_id)
    if not group:
        raise HTTPException(404)
    return group


@router.post("/")
async def create_group(
    data: GroupCreateUpdate,
    auth_data: admin_dep,
    service: group_service_dep,
) -> Group:
    return await service.upsert_group(data)


@router.put("/{group_id}")
async def update_group(
    group_id: UUID,
    data: GroupCreateUpdate,
    auth_data: admin_dep,
    service: group_service_dep,
) -> Group:
    return await service.upsert_group(data, group_id)
