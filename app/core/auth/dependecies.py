from fastapi import Depends
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.exceptions import (
    ClaimValidationError,
    raise_invalid_claims_exception,
)
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.auth.schemas import AuthData
from app.core.config import settings


async def verify_and_get_auth_data(
    session=(Depends(verify_session()) if not settings.DEBUG else None),
) -> AuthData:
    if settings.DEBUG:
        return fake_auth_data()

    user_roles = await session.get_claim_value(UserRoleClaim)
    tenant = ""
    roles = []
    for role in user_roles:
        if role.startswith("tenant-"):
            tenant = role.split("-")[1]
        elif role.startswith("role-"):
            roles.append(role.split("-")[1])
        elif role == "status-disabled":
            raise_invalid_claims_exception(
                "User is disabled", [ClaimValidationError(UserRoleClaim.key, None)]
            )
    if tenant == "":
        raise_invalid_claims_exception(
            "Tenant not found", [ClaimValidationError(UserRoleClaim.key, None)]
        )
    return AuthData(tenant_id=tenant, roles=tuple(roles))


# TODO maybe change this to copy a real structure but it works for now
def fake_auth_data():
    user_role = "akkurim_trainer_admin_guardian_athlete"
    tenant_id, *roles = user_role.split("_")
    roles = tuple(roles)
    return AuthData(tenant_id=tenant_id, roles=roles)


async def is_trainer_and_tenant_info(
    auth_data: AuthData = (Depends(verify_and_get_auth_data)),
) -> AuthData:
    if "trainer" not in auth_data.roles:
        raise_invalid_claims_exception(
            "Wrong user config", [ClaimValidationError(UserRoleClaim.key, None)]
        )
    return auth_data


async def is_admin_and_tenant_info(
    auth_data: AuthData = Depends(verify_and_get_auth_data),
) -> AuthData:
    if "admin" not in auth_data.roles:
        raise_invalid_claims_exception(
            "Wrong user config", [ClaimValidationError(UserRoleClaim.key, None)]
        )
    return auth_data


async def is_guardian_and_tenant_info(
    auth_data: AuthData = (
        Depends(verify_and_get_auth_data)
        if not settings.DEBUG
        else Depends(fake_auth_data)
    ),
) -> AuthData:
    if "guardian" not in auth_data.roles:
        raise_invalid_claims_exception(
            "Wrong user config", [ClaimValidationError(UserRoleClaim.key, None)]
        )
    return auth_data


async def is_athlete_and_tenant_info(
    auth_data: AuthData = (
        Depends(verify_and_get_auth_data)
        if not settings.DEBUG
        else Depends(fake_auth_data)
    ),
) -> AuthData:
    if "athlete" not in auth_data.roles:
        raise_invalid_claims_exception(
            "Wrong user config", [ClaimValidationError(UserRoleClaim.key, None)]
        )
    return auth_data
