from typing import Annotated, Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from app.core.auth import admin_dep, trainer_dep
from app.models import Athlete, Group

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
