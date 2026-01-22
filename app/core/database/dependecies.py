from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import AuthData, verify_and_get_auth_data
from app.core.config import settings

from .config import db_settings


class SQLDatabase:
    """Manage SQLAlchemy async engine and sessionmaker similarly to `Database`.

    Call `connect()` at app startup to create the engine, and `disconnect()` at
    shutdown to dispose it. `get_sessionmaker()` returns a sessionmaker bound
    to the engine.
    """

    def __init__(self):
        self.engine = None
        self._sessionmaker = None

    async def connect(self):
        if self.engine is None:
            self.engine = create_async_engine(
                db_settings.DATABASE_URL,
                echo=settings.DEBUG,
                future=True,
            )
            self._sessionmaker = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )

    async def disconnect(self):
        if self.engine is not None:
            try:
                await self.engine.dispose()
            finally:
                self.engine = None
                self._sessionmaker = None

    def get_sessionmaker(self):
        if self._sessionmaker is None:
            # Lazily create a sessionmaker if engine already exists or create a
            # temporary engine. Prefer calling `connect()` at startup.
            if self.engine is None:
                self.engine = create_async_engine(
                    db_settings.DATABASE_URL, echo=settings.DEBUG, future=True
                )
            self._sessionmaker = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
        return self._sessionmaker


sa_db = SQLDatabase()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sa_db.get_sessionmaker()
    async with async_session() as session:
        yield session


async def get_tenant_db(
    auth_data: AuthData = Depends(verify_and_get_auth_data),
) -> AsyncGenerator[AsyncSession, None]:
    async_session = sa_db.get_sessionmaker()
    async with async_session() as session:
        await session.execute(text(f'SET search_path TO "{auth_data.tenant_id}"'))
        yield session
