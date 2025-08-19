from typing import Optional

from pydantic import UUID1, AwareDatetime, EmailStr

from app.core.shared.base_schema import BaseSchema, generate_example_values


class GuardianBase(BaseSchema):
    id: UUID1
    bank_number: Optional[str]
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str]
    deleted_at: Optional[AwareDatetime]


class GuardianCreate(GuardianBase):
    pass


class GuardianCreatePublic(GuardianCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GuardianCreate),
            ],
        }
    }


class GuardianUpdate(GuardianBase):
    updated_at: AwareDatetime


class GuardianUpdatePublic(GuardianUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GuardianUpdate),
            ],
        }
    }


class GuardianRead(GuardianBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class GuardianReadPublic(GuardianRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GuardianRead),
            ],
        }
    }
