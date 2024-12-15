from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

from app.api.v1 import admin, guardian, remote_config
from app.auth.supertokens_config import supertokens_init
from app.config import settings
from app.db.database import lifespan

supertokens_init()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.add_middleware(get_middleware())
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.WEBSITE_DOMAIN,
        settings.API_DOMAIN,
        settings.PUBLIC_DOMAIN,
    ],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)
app.include_router(admin.router)
app.include_router(guardian.router)
app.include_router(remote_config.router)


@app.get("/")
def read_root():
    return {"Hello": "Dev1"}


""" @app.get(
    "/test",
    response_model=test_schema.TestBase,
)
async def read_test(
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(Test))
    return res.scalars().first()


@app.get(
    "/protected-test",
    response_model=test_schema.TestBase,
    responses={401: {"description": "Unauthorized"}},
)
async def read_test(
    session: SessionContainer = Depends(verify_session()),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(Test))
    return res.scalars().first()
"""
