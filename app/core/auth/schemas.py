from pydantic.json_schema import SkipJsonSchema
from sqlmodel import SQLModel
from supertokens_python.recipe.session import SessionContainer


class AuthData(SQLModel):
    tenant_id: str
    roles: tuple[str, ...]
    session: SkipJsonSchema[SessionContainer]
    email: str | None = None

    class Config:
        arbitrary_types_allowed = True
