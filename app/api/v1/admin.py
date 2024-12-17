from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Response, status
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim
from supertokens_python.recipe.userroles.asyncio import (
    add_role_to_user,
    create_new_role_or_add_permissions,
)

from app.db.database import get_db
from app.schemas.remote_config import RemoteConfigBase

router = APIRouter(
    prefix="/v1/admin",
    tags=["admin"],
    include_in_schema=False,
    responses={
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
    },
    dependencies=[Depends(verify_session())],
)
SessionType = Annotated[SessionContainer, Depends(verify_session())]
DBConection = Annotated[Connection, Depends(get_db)]


@router.put(
    "/remote-config/{remote_config_id}",
    status_code=204,
)
async def update_remote_config(
    session: SessionType,
    remote_config_data: RemoteConfigBase,
    db: DBConection,
):
    roles = await session.get_claim_value(UserRoleClaim)
    if roles is None or "admin" not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await db.execute(
        """UPDATE remote_config SET server_url = $2, websocket_url = $3, 
        dev_prefix = $4, welcome_message = $5, minimum_app_version = $6
        WHERE id = $1""",
        remote_config_data.id,
        remote_config_data.server_url,
        remote_config_data.websocket_url,
        remote_config_data.dev_prefix,
        remote_config_data.welcome_message,
        remote_config_data.minimum_app_version,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
