from sqlmodel import SQLModel
from supertokens_python.recipe.session import SessionContainer


class AuthData(SQLModel):
    tenant_id: str
    roles: tuple[str, ...]
    session: SessionContainer
    email: str | None = None
