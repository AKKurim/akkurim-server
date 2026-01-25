from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from supertokens_python.recipe.emailpassword.asyncio import (
    sign_in,
    update_email_or_password,
)
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.asyncio import revoke_all_sessions_for_user
from supertokens_python.recipe.session.framework.fastapi import verify_session

from app.core.auth import auth_data_dep
from app.core.database import get_tenant_db
from app.models import Athlete, Guardian

from .schemas import ChangePasswordSchema

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        "200": {"description": "Success"},
        "400": {"description": "Bad Request"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
        # "404": {"description": "Not Found"},
        # "409": {"description": "Conflict"},
    },
    default_response_class=ORJSONResponse,
)
db_dep = Annotated[AsyncSession, Depends(get_tenant_db)]


# --- 1. CHANGE PASSWORD ENDPOINT ---
@router.post("/change-password", include_in_schema=False)
async def change_password(
    data: ChangePasswordSchema,
    auth_data: auth_data_dep,
):
    # 2. Verify Old Password by attempting a "Sign In"
    # This is the safest way to check if 'oldPassword' is correct
    signin_response = await sign_in(
        auth_data.email, data.old_password, user_context=None
    )

    if signin_response.status != "OK":
        # Usually means WRONG_CREDENTIALS_ERROR
        raise HTTPException(status_code=400, detail="Current password is incorrect.")

    # 3. Update to New Password
    user_id = auth_data.session.get_user_id()
    update_response = await update_email_or_password(
        user_id, password=data.new_password
    )

    if update_response.status != "OK":
        raise HTTPException(status_code=500, detail="Failed to update password")

    return {"message": "Password updated successfully"}


# --- 2. REVOKE SESSIONS ENDPOINT ---
@router.post("/revoke-all-sessions", include_in_schema=False)
async def revoke_sessions(session: SessionContainer = Depends(verify_session())):
    user_id = session.get_user_id()

    # This kills all tokens (including the current one)
    await revoke_all_sessions_for_user(user_id)

    return {"message": "All sessions revoked"}


@router.get("/me", response_class=ORJSONResponse, response_model=dict[str, str])
async def read_me(
    auth_data: auth_data_dep,
    db: db_dep,
):
    res_dict = {
        "email": auth_data.email,
    }
    if "athlete" in auth_data.roles:
        # read email
        athlete_res = await db.execute(
            select(Athlete).where(Athlete.email == auth_data.email)
        )
        athlete: Athlete | None = athlete_res.scalar_one_or_none()
        if athlete:
            res_dict["first_name"] = athlete.first_name
            res_dict["last_name"] = athlete.last_name
            res_dict["full_name"] = f"{athlete.first_name} {athlete.last_name}"
    if "guardian" in auth_data.roles:
        guardian_res = await db.execute(
            select(Guardian).where(Guardian.email == auth_data.email)
        )
        guardian: Guardian | None = guardian_res.scalar_one_or_none()
        if guardian:
            res_dict["first_name"] = guardian.first_name
            res_dict["last_name"] = guardian.last_name
            res_dict["full_name"] = f"{guardian.first_name} {guardian.last_name}"
    return ORJSONResponse(res_dict, 200)
