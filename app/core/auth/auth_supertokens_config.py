from typing import Optional

from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.asyncio import get_user
from supertokens_python.recipe import dashboard, emailpassword, session, userroles
from supertokens_python.recipe.session.interfaces import RecipeInterface

from app.core.config import settings
from app.core.logging import logger


def override_create_new_session_function(original_implementation: RecipeInterface):
    original_create = original_implementation.create_new_session

    async def custom_create_new_session(
        request,
        user_id: str,
        access_token_payload: Optional[dict] = None,
        session_data: Optional[dict] = None,
        user_context: Optional[dict] = None,
    ):
        access_token_payload = access_token_payload or {}

        user = await get_user(user_id)
        logger.info(f"user  {user}")
        if user:
            access_token_payload["email"] = user.email

        return await original_create(
            request, user_id, access_token_payload, session_data, user_context
        )

    original_implementation.create_new_session = custom_create_new_session
    return original_implementation


def supertokens_init():
    init(
        app_info=InputAppInfo(
            app_name=settings.APP_NAME,
            api_domain=settings.API_DOMAIN,
            website_domain=settings.WEBSITE_DOMAIN,
            api_base_path="/auth",
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.SUPERTOKENS_CONNECTION_URI, api_key=settings.API_KEY
        ),
        framework="fastapi",
        recipe_list=[
            session.init(
                expose_access_token_to_frontend_in_cookie_based_auth=True,
                override=session.InputOverrideConfig(
                    functions=custom_create_new_session
                ),
            ),
            emailpassword.init(),
            dashboard.init(admins=[settings.DASHBOARD_ADMIN]),
            userroles.init(),
        ],
        mode="asgi",
    )
