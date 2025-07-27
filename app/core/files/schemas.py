from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class FileBase(BaseSchema):
    id: UUID1
    name: str
    mime_type: str
    size: int
    type: str
    deleted_at: Optional[AwareDatetime]


class FileCreate(FileBase):
    pass


class FileCreatePublic(FileCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(FileCreate),
            ],
        }
    }


class FileUpdate(FileBase):
    updated_at: AwareDatetime


class FileUpdatePublic(FileUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(FileUpdate),
            ],
        }
    }


class FileRead(FileBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class FileReadPublic(FileRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(FileRead),
            ],
        }
    }
