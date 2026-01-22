from typing import Any, Dict, Optional, Union

from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.asyncio import get_user
from supertokens_python.recipe import dashboard, emailpassword, session, userroles
from supertokens_python.recipe.emailpassword import InputFormField, InputSignUpFeature

from app.core.config import settings


def supertokens_init():
    # lazy import to avoid circular import when app.core.database depends on app.core.auth
    from .registration_override import override_email_password_apis

    init(
        app_info=InputAppInfo(
            app_name=settings.APP_NAME,
            api_domain=settings.API_DOMAIN,
            website_domain=settings.WEBSITE_DOMAIN,
            api_base_path="/auth",
            website_base_path="/auth",
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.SUPERTOKENS_CONNECTION_URI, api_key=settings.API_KEY
        ),
        framework="fastapi",
        recipe_list=[
            session.init(
                expose_access_token_to_frontend_in_cookie_based_auth=True,
                cookie_same_site="none",  # to allow cross-site cookies
                cookie_secure=True,  # to allow cookies over HTTPS only
            ),
            emailpassword.init(
                override=emailpassword.InputOverrideConfig(
                    apis=override_email_password_apis,
                ),
                sign_up_feature=InputSignUpFeature(
                    form_fields=[
                        InputFormField(id="tenant", optional=False),
                    ]
                ),
            ),
            dashboard.init(admins=[settings.DASHBOARD_ADMIN]),
            userroles.init(),
        ],
        mode="asgi",
    )
