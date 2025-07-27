from typing import Annotated, Optional

from pydantic import UUID1, AfterValidator, AwareDatetime, EmailStr

from app.core.shared.base_schema import BaseSchema, generate_example_values
from app.features.athlete.utils import validate_birth_number


class AthleteBase(BaseSchema):
    id: UUID1
    bank_number: Optional[str]
    birth_number: Annotated[str, AfterValidator(validate_birth_number)]
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
    profile_image_id: Optional[UUID1]
    status: str
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


class SignUpFormBase(BaseSchema):
    id: UUID1
    birth_number: Annotated[str, AfterValidator(validate_birth_number)]
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
    status: str
    school_year_id: UUID1
    times_per_week: int
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


class PointsBase(BaseSchema):
    type: str
    source_id: UUID1
    amount: int
    athlete_id: UUID1
    deleted_at: Optional[AwareDatetime]


class PointsCreate(PointsBase):
    pass


class PointsCreatePublic(PointsCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(PointsCreate),
            ],
        }
    }


class PointsUpdate(PointsBase):
    updated_at: AwareDatetime


class PointsUpdatePublic(PointsUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(PointsUpdate),
            ],
        }
    }


class PointsRead(PointsBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class PointsReadPublic(PointsRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(PointsRead),
            ],
        }
    }
