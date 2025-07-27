import decimal
from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class PaymentBase(BaseSchema):
    id: int
    type: str
    amount: decimal.Decimal
    status: str
    from_id: Optional[UUID1]  # if None then the club is the payer
    to_id: Optional[UUID1]
    description: Optional[str]
    deleted_at: Optional[AwareDatetime]


class PaymentCreate(PaymentBase):
    pass


class PaymentCreatePublic(PaymentCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(PaymentCreate),
            ],
        }
    }


class PaymentUpdate(PaymentBase):
    updated_at: AwareDatetime


class PaymentUpdatePublic(PaymentUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(PaymentUpdate),
            ],
        }
    }


class PaymentRead(PaymentBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class PaymentReadPublic(PaymentRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(PaymentRead),
            ],
        }
    }
