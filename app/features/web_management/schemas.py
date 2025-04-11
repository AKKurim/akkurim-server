from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class WebPostBase(BaseSchema):
    id: UUID1
    title: str
    content: str
    trainer_id: UUID1
    deleted_at: Optional[AwareDatetime]


class WebPostCreate(WebPostBase):
    pass


class WebPostCreatePublic(WebPostCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(WebPostCreate),
            ],
        }
    }


class WebPostUpdate(WebPostBase):
    updated_at: AwareDatetime


class WebPostUpdatePublic(WebPostUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(WebPostUpdate),
            ],
        }
    }


class WebPostRead(WebPostBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class WebPostReadPublic(WebPostRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(WebPostRead),
            ],
        }
    }
