import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

from app.api.v1 import admin, guardian, remote_config, sse
from app.auth.supertokens_config import supertokens_init
from app.config import settings
from app.db.database import db
from app.utils.broadcast import broadcast


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.connect()
        await broadcast.connect()
        yield
    finally:
        await db.disconnect()
        await broadcast.disconnect()


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
app.include_router(sse.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def read_root():
    return {"Status": "Working", "App": settings.APP_NAME}


# for testing purposes
@app.post("/fake-sync-endpoint")
async def fake_sync_endpoint():
    # simulate fake data processing by sleeping for 0.5 seconds
    await asyncio.sleep(2)
    return {"message": "Synced"}
