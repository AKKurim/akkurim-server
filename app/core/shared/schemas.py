from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class SchoolYearBase(BaseSchema):
    id: UUID1
    name: str
    deleted_at: Optional[AwareDatetime]


class SchoolYearCreate(SchoolYearBase):
    pass


class SchoolYearCreatePublic(SchoolYearCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SchoolYearCreate),
            ],
        }
    }


class SchoolYearUpdate(SchoolYearBase):
    updated_at: AwareDatetime


class SchoolYearUpdatePublic(SchoolYearUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SchoolYearUpdate),
            ],
        }
    }


class SchoolYearRead(SchoolYearBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class SchoolYearReadPublic(SchoolYearRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SchoolYearRead),
            ],
        }
    }
