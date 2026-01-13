from uuid import UUID

from sqlmodel import Field

from ._base_model import BaseModel


# BASE model inheritance later, now only for testing migrations
class SchoolYear(BaseModel, table=True):
    __tablename__ = "school_year"

    id: UUID = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
