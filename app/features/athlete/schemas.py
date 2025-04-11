from typing import Annotated, Optional

from pydantic import UUID1, AfterValidator, AwareDatetime, EmailStr

from app.core.shared.base_schema import BaseSchema, generate_example_values
from app.features.athlete.utils import pydanyic_validate_birth_number


class AthleteBase(BaseSchema):
    id: UUID1
    birth_number: Annotated[str, AfterValidator(pydanyic_validate_birth_number)]
    first_name: str
    last_name: str
    street: str
    city: str
    zip: str
    email: Optional[EmailStr]
    phone: Optional[str]
    ean: Optional[str]
    note: Optional[str]
    club_id: str
    profile_picture: Optional[str]
    athlete_status_id: UUID1
    deleted_at: Optional[AwareDatetime]


class AthleteCreate(AthleteBase):
    pass


class AthleteCreatePublic(AthleteCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteCreate),
            ],
        }
    }


class AthleteUpdate(AthleteBase):
    updated_at: AwareDatetime


class AthleteUpdatePublic(AthleteUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteUpdate),
            ],
        }
    }


class AthleteRead(AthleteBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class AthleteReadPublic(AthleteRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteRead),
            ],
        }
    }


class AthleteStatusBase(BaseSchema):
    id: UUID1
    name: str
    description: Optional[str]
    deleted_at: Optional[AwareDatetime]


class AthleteStatusCreate(AthleteStatusBase):
    pass


class AthleteStatusCreatePublic(AthleteStatusCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteStatusCreate),
            ],
        }
    }


class AthleteStatusUpdate(AthleteStatusBase):
    updated_at: AwareDatetime


class AthleteStatusUpdatePublic(AthleteStatusUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteStatusUpdate),
            ],
        }
    }


class AthleteStatusRead(AthleteStatusBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class AthleteStatusReadPublic(AthleteStatusRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteStatusRead),
            ],
        }
    }


class SignUpFormBase(BaseSchema):
    id: UUID1
    birth_number: Annotated[str, AfterValidator(pydanyic_validate_birth_number)]
    first_name: str
    last_name: str
    street: str
    city: str
    zip: str
    email: Optional[EmailStr]
    phone: Optional[str]
    guardian_first_name1: str
    guardian_last_name1: str
    guardian_email1: EmailStr
    guardian_phone1: str
    guardian_first_name2: Optional[str]
    guardian_last_name2: Optional[str]
    guardian_email2: Optional[EmailStr]
    guardian_phone2: Optional[str]
    note: Optional[str]
    sign_up_form_status_id: UUID1
    school_year_id: UUID1
    deleted_at: Optional[AwareDatetime]


class SignUpFormCreate(SignUpFormBase):
    pass


class SignUpFormCreatePublic(SignUpFormCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SignUpFormCreate),
            ],
        }
    }


class SignUpFormUpdate(SignUpFormBase):
    updated_at: AwareDatetime


class SignUpFormUpdatePublic(SignUpFormUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SignUpFormUpdate),
            ],
        }
    }


class SignUpFormRead(SignUpFormBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class SignUpFormReadPublic(SignUpFormRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SignUpFormRead),
            ],
        }
    }


class SignUpFormStatusBase(BaseSchema):
    id: UUID1
    name: str
    description: Optional[str]
    deleted_at: Optional[AwareDatetime]


class SignUpFormStatusCreate(SignUpFormStatusBase):
    pass


class SignUpFormStatusCreatePublic(SignUpFormStatusCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SignUpFormStatusCreate),
            ],
        }
    }


class SignUpFormStatusUpdate(SignUpFormStatusBase):
    updated_at: AwareDatetime


class SignUpFormStatusUpdatePublic(SignUpFormStatusUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SignUpFormStatusUpdate),
            ],
        }
    }


class SignUpFormStatusRead(SignUpFormStatusBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class SignUpFormStatusReadPublic(SignUpFormStatusRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SignUpFormStatusRead),
            ],
        }
    }
