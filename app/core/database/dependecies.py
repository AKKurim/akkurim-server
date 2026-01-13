from typing import AsyncGenerator

import asyncpg
from asyncpg import Connection
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth.dependecies import verify_and_get_auth_data
from app.core.auth.schemas import AuthData
from app.core.config import settings


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"),
            min_size=settings.MIN_CONNECTIONS,
            max_size=settings.MAX_CONNECTIONS,
        )

    async def disconnect(self):
        await self.pool.close()


db = Database()


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def get_tenant_db(
    auth_data: AuthData = Depends(verify_and_get_auth_data),
) -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        await session.execute(text(f'SET search_path TO "{auth_data.tenant_id}"'))
        yield session


async def get_db():
    async with db.pool.acquire() as connection:
        try:
            yield connection
        finally:
            connection: Connection
            await connection.close()
