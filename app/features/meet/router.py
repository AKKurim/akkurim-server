from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from pydantic import AwareDatetime
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import AuthData, admin_dep, trainer_dep
from app.core.database import get_tenant_db
from app.models import Meet

from .service import MeetService

router = APIRouter(
    prefix="/meet",
    tags=["meet"],
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
service_dep = Annotated[MeetService, Depends(MeetService)]


@router.get(
    "/{meet_id}",
    response_model=Any,
)
async def get_meet_by_id(
    meet_id: str,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> Meet:
    return await service.get_meet_by_id(
        meet_id,
        db,
    )


@router.post(
    "/sync/cas/{external_meet_id}",
    response_model=Any,
    status_code=status.HTTP_201_CREATED,
)
async def sync_meet_from_cas(
    external_meet_id: str,
    auth_data: admin_dep,
    db: db_dep,
    service: service_dep,
    type: str = "CAS",
    use_private_registrations: bool = False,
) -> Meet:
    return await service.sync_meet_from_cas(
        db,
        external_meet_id,
        type,
        use_private_registrations,
    )
