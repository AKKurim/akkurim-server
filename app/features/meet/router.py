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
from app.core.database import get_db
from app.features.meet.schemas import MeetEventReadPublic
from app.features.meet.service import MeetEventService

router = APIRouter(
    prefix="/meet_event",
    tags=["meet_event"],
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
        Depends(MeetEventService),
    ],
    default_response_class=ORJSONResponse,
)
trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
admin_dep = Annotated[AuthData, Depends(is_admin_and_tenant_info)]
db_dep = Annotated[Connection, Depends(get_db)]
service_dep = Annotated[MeetEventService, Depends(MeetEventService)]


@router.get(
    "/{meet_id}",
    response_model=list[MeetEventReadPublic],
)
async def read_discipline(
    meet_id: str,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> list[MeetEventReadPublic]:
    meet_events = await service.get_meet_events_by_meet_id(
        auth_data.tenant_id,
        meet_id,
        db,
    )
    return ORJSONResponse(meet_events, status_code=status.HTTP_200_OK)
