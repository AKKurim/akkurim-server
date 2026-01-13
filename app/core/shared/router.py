from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from pydantic import UUID1
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth.dependecies import (
    is_admin_and_tenant_info,
    is_trainer_and_tenant_info,
    verify_and_get_auth_data,
)
from app.core.auth.schemas import AuthData
from app.core.database import get_db, get_tenant_db
from app.core.shared.schemas import SchoolYearCreatePublic, SchoolYearReadPublic
from app.core.shared.service import SchoolYearService
from app.models import SchoolYear

router = APIRouter(
    prefix="",
    tags=["shared"],
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
    ],
    default_response_class=ORJSONResponse,
)

admin_dep = Annotated[AuthData, Depends(is_admin_and_tenant_info)]
db_dep = Annotated[AsyncSession, Depends(get_tenant_db)]
service_dep = Annotated[SchoolYearService, Depends(SchoolYearService)]
trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
auth_data_dep = Annotated[AuthData, Depends(verify_and_get_auth_data)]


@router.post(
    "/school_year",
    response_model=SchoolYearReadPublic,
)
async def create_school_year(
    school_year: SchoolYearCreatePublic,
    auth_data: admin_dep,
    db: db_dep,
    service: service_dep,
) -> SchoolYearReadPublic:
    return await service.create_school_year(
        auth_data.tenant_id,
        school_year.model_dump(),
        db,
    )


@router.get(
    "/school_year/{school_year_id}",
    response_model=SchoolYearReadPublic,
)
async def read_school_year(
    school_year_id: UUID1,
    auth_data: auth_data_dep,
    db: db_dep,
    service: service_dep,
) -> SchoolYearReadPublic:
    return await service.get_school_year_by_id(
        auth_data.tenant_id,
        school_year_id,
        db,
    )


@router.get(
    "/school_year/",
    response_model=list[SchoolYear],
)
async def read_all_school_years(
    auth_data: auth_data_dep,
    db: db_dep,
    service: service_dep,
) -> list[SchoolYear]:
    # return await service.get_all_school_years(
    #     auth_data.tenant_id,
    #     db,
    # )
    statement = select(SchoolYear).where(SchoolYear.deleted_at.is_(None))
    results = await db.exec(statement)
    return results.all()
