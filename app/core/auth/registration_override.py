# Make sure you import APIInterface, not RecipeInterface
from sqlalchemy import select, text
from sqlmodel.ext.asyncio.session import AsyncSession
from supertokens_python.recipe.emailpassword.interfaces import (
    APIInterface,
    APIOptions,
    SignUpPostNotAllowedResponse,
)
from supertokens_python.recipe.userroles import UserRoleClaim
from supertokens_python.recipe.userroles.asyncio import add_role_to_user

from app.core.database import db_settings, sa_db
from app.models import Athlete, Guardian, Helper, Trainer


# Define the override for APIs
def override_email_password_apis(original_implementation: APIInterface):
    original_sign_up_post = original_implementation.sign_up_post

    async def sign_up_post(
        form_fields, tenant_id, api_options, user_context, *args, **kwargs
    ):
        ##important tenant is not the same as tenant_id
        email = next(
            (field.value for field in form_fields if field.id == "email"), None
        )
        tenant = next(
            (field.value for field in form_fields if field.id == "tenant"), None
        )
        if tenant is None or tenant not in db_settings.ACTIVE_TENANTS:
            return SignUpPostNotAllowedResponse("Invalid tenant")
        async_session = sa_db.get_sessionmaker()
        async with async_session() as session:
            session: AsyncSession
            await session.execute(text(f'SET search_path TO "{tenant}"'))
            athlete_result = await session.execute(
                select(Athlete).where(Athlete.email == email)
            )
            athlete = athlete_result.scalars().one_or_none()
            guardian_result = await session.execute(
                select(Guardian).where(Guardian.email == email)
            )
            guardian = guardian_result.scalars().one_or_none()
            helper_result = await session.execute(
                select(Helper).where(Helper.email == email)
            )
            helper = helper_result.scalars().one_or_none()
            if athlete is None and guardian is None and helper is None:
                return SignUpPostNotAllowedResponse("Email nenalezen v databázi.")

        # 1. Call original (Pass ALL arguments, including tenant_id)
        response = await original_sign_up_post(
            form_fields, tenant_id, api_options, user_context, *args, **kwargs
        )

        if response.status == "OK":
            user_id = response.user.id
            role_to_assign = f"tenant-{tenant}"
            await add_role_to_user(
                tenant_id=tenant_id,
                user_id=user_id,
                role=role_to_assign,
            )

            async_session = sa_db.get_sessionmaker()
            async with async_session() as session:
                session: AsyncSession
                await session.execute(text(f'SET search_path TO "{tenant}"'))
                athlete_result = await session.execute(
                    select(Athlete).where(Athlete.email == email)
                )
                athlete = athlete_result.scalars().one_or_none()
                # athlete and trainer roles
                if athlete:
                    await add_role_to_user(
                        tenant_id=tenant_id,
                        user_id=user_id,
                        role="role-athlete",
                    )
                    trainer_result = await session.execute(
                        select(Trainer).where(Trainer.athlete_id == athlete.id)
                    )
                    trainer = trainer_result.scalars().one_or_none()
                    if trainer:
                        await add_role_to_user(
                            tenant_id=tenant_id,
                            user_id=user_id,
                            role="role-trainer",
                        )
                # guardian role independently
                guardian_result = await session.execute(
                    select(Guardian).where(Guardian.email == email)
                )
                guardian = guardian_result.scalars().one_or_none()
                if guardian:
                    await add_role_to_user(
                        tenant_id=tenant_id,
                        user_id=user_id,
                        role="role-guardian",
                    )
                # helper role independently TODO

            if response.session:
                await response.session.fetch_and_set_claim(UserRoleClaim)

        return response

    original_implementation.sign_up_post = sign_up_post
    return original_implementation
