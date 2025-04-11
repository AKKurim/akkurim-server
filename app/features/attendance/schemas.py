from datetime import time
from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class GroupBase(BaseSchema):
    id: UUID1
    name: str
    description: str
    training_time_id: UUID1
    school_year_id: UUID1
    deleted_at: Optional[AwareDatetime]


class GroupCreate(GroupBase):
    pass


class GroupCreatePublic(GroupCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GroupCreate),
            ],
        }
    }


class GroupUpdate(GroupBase):
    updated_at: AwareDatetime


class GroupUpdatePublic(GroupUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GroupUpdate),
            ],
        }
    }


class GroupRead(GroupBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class GroupReadPublic(GroupRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GroupRead),
            ],
        }
    }


class TrainingBase(BaseSchema):
    id: UUID1
    group_id: UUID1
    datetime_: AwareDatetime
    duration_minutes: int
    description: str
    deleted_at: Optional[AwareDatetime]


class TrainingCreate(TrainingBase):
    pass


class TrainingCreatePublic(TrainingCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainingCreate),
            ],
        }
    }


class TrainingUpdate(TrainingBase):
    updated_at: AwareDatetime


class TrainingUpdatePublic(TrainingUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainingUpdate),
            ],
        }
    }


class TrainingRead(TrainingBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class TrainingReadPublic(TrainingRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainingRead),
            ],
        }
    }


class TrainingTimeBase(BaseSchema):
    id: UUID1
    day: str
    summer_time: time
    winter_time: time
    deleted_at: Optional[AwareDatetime]


class TrainingTimeCreate(TrainingTimeBase):
    pass


class TrainingTimeCreatePublic(TrainingTimeCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainingTimeCreate),
            ],
        }
    }


class TrainingTimeUpdate(TrainingTimeBase):
    updated_at: AwareDatetime


class TrainingTimeUpdatePublic(TrainingTimeUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainingTimeUpdate),
            ],
        }
    }


class TrainingTimeRead(TrainingTimeBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class TrainingTimeReadPublic(TrainingTimeRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainingTimeRead),
            ],
        }
    }
