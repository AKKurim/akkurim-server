from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import AuthData, is_trainer_and_tenant_info
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

trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
