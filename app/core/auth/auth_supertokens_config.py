from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.asyncio import get_user
from supertokens_python.recipe import dashboard, emailpassword, session, userroles
from supertokens_python.recipe.session.interfaces import RecipeInterface

from app.core.config import settings
from app.core.logging import logger


def custom_create_new_session(input_: RecipeInterface):
    original_create = input_.create_new_session

    async def override_create_new_session(
        user_id, access_token_payload=None, session_data=None, user_context=None
    ):
        access_token_payload = access_token_payload or {}

        # Fetch user email using Supertokens user_id
        logger.info("fetching user email")
        user = await get_user(user_id)
        logger.info(f"fetched user email: {user}")
        if user is not None:
            access_token_payload["email"] = user.email

        return await original_create(
            user_id, access_token_payload, session_data, user_context
        )

    input_.create_new_session = override_create_new_session
    return input_


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
