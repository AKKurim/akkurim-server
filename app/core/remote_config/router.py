from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.core.database import get_db
from app.core.remote_config.schemas import RemoteConfigReadPublic
from app.core.remote_config.service import RemoteConfigService

router = APIRouter(
    prefix="/remote-config",
    tags=["remote-config"],
    responses={},
    dependencies=[
        Depends(get_db),
    ],
    default_response_class=ORJSONResponse,
)

db_dep = Annotated[Connection, Depends(get_db)]
service_dep = Annotated[RemoteConfigService, Depends(RemoteConfigService)]


@router.get(
    "/",
    response_model=RemoteConfigReadPublic,
)
async def get_remote_config(db: db_dep, service: service_dep) -> RemoteConfigReadPublic:
    remote_config = await service.get_remote_config("public", db)
    return ORJSONResponse(remote_config, status_code=200)
