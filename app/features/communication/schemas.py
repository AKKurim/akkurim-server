from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class RequestBase(BaseSchema):
    id: UUID1
    status: str
    type: str
    person_id: UUID1
    item_id: Optional[UUID1]
    name: str
    description: Optional[str]
    deleted_at: Optional[AwareDatetime]


class RequestCreate(RequestBase):
    pass


class RequestCreatePublic(RequestCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RequestCreate),
            ],
        }
    }


class RequestUpdate(RequestBase):
    updated_at: AwareDatetime


class RequestUpdatePublic(RequestUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RequestUpdate),
            ],
        }
    }


class RequestRead(RequestBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class RequestReadPublic(RequestRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RequestRead),
            ],
        }
    }


class ResponseBase(BaseSchema):
    id: UUID1
    request_id: UUID1
    person_type: str
    person_id: UUID1
    file_id: Optional[UUID1]
    description: str
    deleted_at: Optional[AwareDatetime]


class ResponseCreate(ResponseBase):
    pass


class ResponseCreatePublic(ResponseCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ResponseCreate),
            ],
        }
    }


class ResponseUpdate(ResponseBase):
    updated_at: AwareDatetime


class ResponseUpdatePublic(ResponseUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ResponseUpdate),
            ],
        }
    }


class ResponseRead(ResponseBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class ResponseReadPublic(ResponseRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ResponseRead),
            ],
        }
    }
