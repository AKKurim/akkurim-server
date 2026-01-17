from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from pydantic import AwareDatetime
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth.dependecies import (
    is_admin_and_tenant_info,
    is_trainer_and_tenant_info,
)
from app.core.auth.schemas import AuthData
from app.core.database import get_tenant_db
from app.core.sync.service import SyncService

router = APIRouter(
    prefix="/sync",
    tags=["sync"],
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

trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
admin_dep = Annotated[AuthData, Depends(is_admin_and_tenant_info)]
db_dep = Annotated[AsyncSession, Depends(get_tenant_db)]
service_dep = Annotated[SyncService, Depends(SyncService)]


@router.get(
    "/tables/",
    response_model=list[str],
)
async def get_tables_to_sync(
    from_date: AwareDatetime,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[str]:
    return await service.get_tables_to_sync(
        auth_data.tenant_id,
        from_date,
        db,
    )


@router.get(
    "/{table_name}",
    response_model=list[dict],
)
async def get_objects_to_sync(
    table_name: str,
    from_date: AwareDatetime,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[dict]:
    return await service.get_objects_to_sync(
        auth_data.tenant_id,
        table_name,
        from_date,
        db,
    )


@router.post(
    "/{table_name}",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def post_objects_to_sync(
    table_name: str,
    data: dict[str, Any],
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> None:
    await service.sync_objects(
        auth_data.tenant_id,
        table_name,
        data["data"],
        data["primary_keys"],
        db,
    )
    return ORJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=None,
    )
