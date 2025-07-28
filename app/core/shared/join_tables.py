from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class AthleteGuardainBase(BaseSchema):
    athlete_id: UUID1
    guardian_id: UUID1
    deleted_at: Optional[AwareDatetime]


class AthleteGuardainCreate(AthleteGuardainBase):
    pass


class AthleteGuardainUpdate(AthleteGuardainBase):
    updated_at: AwareDatetime


class AthleteGuardainRead(AthleteGuardainBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class AthleteGuardainReadPublic(AthleteGuardainRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteGuardainRead),
            ],
        }
    }


class GroupAthleteBase(BaseSchema):
    group_id: UUID1
    athlete_id: UUID1
    deleted_at: Optional[AwareDatetime]


class GroupAthleteCreate(GroupAthleteBase):
    pass


class GroupAthleteUpdate(GroupAthleteBase):
    updated_at: AwareDatetime


class GroupAthleteRead(GroupAthleteBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class GroupAthleteReadPublic(GroupAthleteRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GroupAthleteRead),
            ],
        }
    }


class GroupAthleteBase(BaseSchema):
    group_id: UUID1
    athlete_id: UUID1
    deleted_at: Optional[AwareDatetime]


class GroupAthleteCreate(GroupAthleteBase):
    pass


class GroupAthleteUpdate(GroupAthleteBase):
    updated_at: AwareDatetime


class GroupAthleteRead(GroupAthleteBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class GroupAthleteReadPublic(GroupAthleteRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GroupAthleteRead),
            ],
        }
    }


class GroupTrainerBase(BaseSchema):
    group_id: UUID1
    trainer_id: UUID1
    deleted_at: Optional[AwareDatetime]


class GroupTrainerCreate(GroupTrainerBase):
    pass


class GroupTrainerUpdate(GroupTrainerBase):
    updated_at: AwareDatetime


class GroupTrainerRead(GroupTrainerBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class GroupTrainerReadPublic(GroupTrainerRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(GroupTrainerRead),
            ],
        }
    }


class TrainingAthleteBase(BaseSchema):
    training_id: UUID1
    athlete_id: UUID1
    presence: str
    deleted_at: Optional[AwareDatetime]


class TrainingAthleteCreate(TrainingAthleteBase):
    pass


class TrainingAthleteUpdate(TrainingAthleteBase):
    updated_at: AwareDatetime


class TrainingAthleteRead(TrainingAthleteBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class TrainingAthleteReadPublic(TrainingAthleteRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainingAthleteRead),
            ],
        }
    }


class TrainingTrainerBase(BaseSchema):
    training_id: UUID1
    trainer_id: UUID1
    presence: str
    deleted_at: Optional[AwareDatetime]


class TrainingTrainerCreate(TrainingTrainerBase):
    pass


class TrainingTrainerUpdate(TrainingTrainerBase):
    updated_at: AwareDatetime


class TrainingTrainerRead(TrainingTrainerBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class TrainingTrainerReadPublic(TrainingTrainerRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(TrainingTrainerRead),
            ],
        }
    }


class AthleteMeetEventBase(BaseSchema):
    athlete_id: UUID1
    meet_event_id: UUID1
    result: Optional[str] = None
    wind: Optional[str] = None
    pb_sb: Optional[str] = None
    points: Optional[str] = None
    deleted_at: Optional[AwareDatetime]


class AthleteMeetEventCreate(AthleteMeetEventBase):
    pass


class AthleteMeetEventUpdate(AthleteMeetEventBase):
    updated_at: AwareDatetime


class AthleteMeetEventRead(AthleteMeetEventBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class AthleteMeetEventReadPublic(AthleteMeetEventRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteMeetEventRead),
            ],
        }
    }


class AthleteSignUpFormBase(BaseSchema):
    athlete_id: UUID1
    sign_up_form_id: UUID1
    deleted_at: Optional[AwareDatetime]


class AthleteSignUpFormCreate(AthleteSignUpFormBase):
    pass


class AthleteSignUpFormUpdate(AthleteSignUpFormBase):
    updated_at: AwareDatetime


class AthleteSignUpFormRead(AthleteSignUpFormBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class AthleteSignUpFormReadPublic(AthleteSignUpFormRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteSignUpFormRead),
            ],
        }
    }


class SignUpFormGroupBase(BaseSchema):
    sign_up_form_id: UUID1
    group_id: UUID1
    deleted_at: Optional[AwareDatetime]


class SignUpFormGroupCreate(SignUpFormGroupBase):
    pass


class SignUpFormGroupUpdate(SignUpFormGroupBase):
    updated_at: AwareDatetime


class SignUpFormGroupRead(SignUpFormGroupBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class SignUpFormGroupReadPublic(SignUpFormGroupRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(SignUpFormGroupRead),
            ],
        }
    }


class AthleteRegistrationMeetEventBase(BaseSchema):
    athlete_id: UUID1
    meet_event_id: UUID1
    status: str
    deleted_at: Optional[AwareDatetime]


class AthleteRegistrationMeetEventCreate(AthleteRegistrationMeetEventBase):
    pass


class AthleteRegistrationMeetEventUpdate(AthleteRegistrationMeetEventBase):
    updated_at: AwareDatetime


class AthleteRegistrationMeetEventRead(AthleteRegistrationMeetEventBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class AthleteRegistrationMeetEventReadPublic(AthleteRegistrationMeetEventRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteRegistrationMeetEventRead),
            ],
        }
    }


class RequestFileBase(BaseSchema):
    request_id: UUID1
    file_id: UUID1
    deleted_at: Optional[AwareDatetime]


class RequestFileCreate(RequestFileBase):
    pass


class RequestFileUpdate(RequestFileBase):
    updated_at: AwareDatetime


class RequestFileRead(RequestFileBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class RequestFileReadPublic(RequestFileRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RequestFileRead),
            ],
        }
    }
