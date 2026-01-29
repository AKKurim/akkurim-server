import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import (
    get_middleware as supertokens_middleware,
)

from app.core.auth import AuthData, auth_data_dep, supertokens_init
from app.core.config import settings
from app.core.database import sa_db
from app.core.logging import logger
from app.core.logging import router as log_router
from app.core.observation_middleware import ObservationMiddleware
from app.core.sse import broadcast
from app.core.sse import router as sse_router
from app.core.sync import router as sync_router
from app.features.athlete import router as athlete_router
from app.features.meet import router as meet_router
from app.features.trainer import router as trainer_router
from app.features.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await sa_db.connect()
        await broadcast.connect()
        logger.info("APP STARTED")
        yield
    finally:
        await sa_db.disconnect()
        await broadcast.disconnect()
        logger.info("APP STOPPED")


supertokens_init()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.add_middleware(supertokens_middleware())
app.add_middleware(ObservationMiddleware)
origings_list = [
    settings.WEBSITE_DOMAIN,
    settings.API_DOMAIN,
    settings.PUBLIC_DOMAIN,
]
if settings.DEBUG:
    origings_list.append("http://192.168.0.9:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origings_list,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)


app.include_router(log_router)
app.include_router(sync_router, prefix=settings.API_V1_PREFIX)
app.include_router(sse_router, prefix=settings.API_V1_PREFIX)
app.include_router(athlete_router, prefix=settings.API_V1_PREFIX)
app.include_router(meet_router, prefix=settings.API_V1_PREFIX)
app.include_router(trainer_router, prefix=settings.API_V1_PREFIX)
app.include_router(user_router, prefix="")  # user router has its own prefix


@app.get(
    "/",
    response_class=ORJSONResponse,
    response_model=dict[str, str],
)
def read_root():
    content = {"status": "working", "app_name": settings.APP_NAME}
    return ORJSONResponse(content, 200)


@app.get(
    "/auth-data/",
    response_class=ORJSONResponse,
    response_model=AuthData,
)
async def get_auth_data(
    auth_data: auth_data_dep,
):
    return ORJSONResponse(auth_data.model_dump(), 200)


# for testing purposes
@app.post("/fake-sync-endpoint")
async def fake_sync_endpoint():
    # simulate fake data processing by sleeping for 2 seconds
    await asyncio.sleep(2)
    return {"message": "Synced"}
