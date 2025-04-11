from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class TrainerBase(BaseSchema):
    id: UUID1
    athlete_id: UUID1
    trainer_status_id: UUID1
    qualification: str
    salary_per_hour: int
    deleted_at: Optional[AwareDatetime]


class TrainerCreate(TrainerBase):
    pass


class TrainerCreatePublic(TrainerCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainerCreate),
            ],
        }
    }


class TrainerUpdate(TrainerBase):
    updated_at: AwareDatetime


class TrainerUpdatePublic(TrainerUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainerUpdate),
            ],
        }
    }


class TrainerRead(TrainerBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class TrainerReadPublic(TrainerRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainerRead),
            ],
        }
    }


class TrainerStatusBase(BaseSchema):
    id: UUID1
    name: str
    description: str
    deleted_at: Optional[AwareDatetime]


class TrainerStatusCreate(TrainerStatusBase):
    pass


class TrainerStatusCreatePublic(TrainerStatusCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainerStatusCreate),
            ],
        }
    }


class TrainerStatusUpdate(TrainerStatusBase):
    updated_at: AwareDatetime


class TrainerStatusUpdatePublic(TrainerStatusUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainerStatusUpdate),
            ],
        }
    }


class TrainerStatusRead(TrainerStatusBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class TrainerStatusReadPublic(TrainerStatusRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainerStatusRead),
            ],
        }
    }
