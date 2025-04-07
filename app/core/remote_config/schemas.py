from typing import Optional

from pydantic import AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class RemoteConfigBase(BaseSchema):
    id: int
    urgent_message: Optional[str]
    minimum_app_version: str


class RemoteConfigCreate(RemoteConfigBase):
    pass


class RemoteConfigCreatePublic(RemoteConfigCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RemoteConfigCreate),
            ],
        }
    }


class RemoteConfigUpdate(RemoteConfigBase):
    updated_at: AwareDatetime


class RemoteConfigUpdatePublic(RemoteConfigUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RemoteConfigUpdate),
            ],
        }
    }


class RemoteConfigRead(RemoteConfigBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class RemoteConfigReadPublic(RemoteConfigRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RemoteConfigRead),
            ],
        }
    }


class ClubBase(BaseSchema):
    id: int
    name: str
    description: str


class ClubCreate(ClubBase):
    pass


class ClubCreatePublic(ClubCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ClubCreate),
            ],
        }
    }


class ClubUpdate(ClubBase):
    updated_at: AwareDatetime


class ClubUpdatePublic(ClubUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ClubUpdate),
            ],
        }
    }


class ClubRead(ClubBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class ClubReadPublic(ClubRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ClubRead),
            ],
        }
    }
