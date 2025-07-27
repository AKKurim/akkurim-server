from typing import Optional

from pydantic import UUID1, AwareDatetime, PastDate

from app.core.shared.base_schema import BaseSchema, generate_example_values


class HelperBase(BaseSchema):
    id: UUID1
    status: str
    bank_number: str
    first_name: str
    last_name: str
    date_of_birth: Optional[PastDate]
    email: str
    phone_number: Optional[str]
    street: Optional[str]
    city: Optional[str]
    zip: Optional[str]
    qualification: Optional[str]
    preferrence: Optional[str]
    deleted_at: Optional[AwareDatetime]


class HelperCreate(HelperBase):
    pass


class HelperCreatePublic(HelperCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(HelperCreate),
            ],
        }
    }


class HelperUpdate(HelperBase):
    updated_at: AwareDatetime


class HelperUpdatePublic(HelperUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(HelperUpdate),
            ],
        }
    }


class HelperRead(HelperBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class HelperReadPublic(HelperRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(HelperRead),
            ],
        }
    }
