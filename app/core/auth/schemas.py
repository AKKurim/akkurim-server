from sqlmodel import SQLModel


class AuthData(SQLModel):
    tenant_id: str
    roles: tuple[str, ...]
    email: str | None = None
