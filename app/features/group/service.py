from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_tenant_db


class GroupService:
    def __init__(self, db: AsyncSession = Depends(get_tenant_db)):
        self.db: AsyncSession = db
