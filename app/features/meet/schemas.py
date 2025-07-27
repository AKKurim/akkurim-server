from typing import Optional

from pydantic import UUID1, AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class DisciplineBase(BaseSchema):
    id: int
    traditional: int
    discipline_type_id: int
    description: str
    short_description: str
    description_en: str
    short_description_en: str
    deleted_at: Optional[AwareDatetime]


class DisciplineCreate(DisciplineBase):
    pass


class DisciplineCreatePublic(DisciplineCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(DisciplineCreate),
            ],
        }
    }


class DisciplineUpdate(DisciplineBase):
    updated_at: AwareDatetime


class DisciplineUpdatePublic(DisciplineUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(DisciplineUpdate),
            ],
        }
    }


class DisciplineRead(DisciplineBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class DisciplineReadPublic(DisciplineRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(DisciplineRead),
            ],
        }
    }


class DisciplineTypeBase(BaseSchema):
    id: int
    sort: str
    name: str
    description: Optional[str]
    name_en: str
    description_en: Optional[str]
    deleted_at: Optional[AwareDatetime]


class DisciplineTypeCreate(DisciplineTypeBase):
    pass


class DisciplineTypeCreatePublic(DisciplineTypeCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(DisciplineTypeCreate),
            ],
        }
    }


class DisciplineTypeUpdate(DisciplineTypeBase):
    updated_at: AwareDatetime


class DisciplineTypeUpdatePublic(DisciplineTypeUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(DisciplineTypeUpdate),
            ],
        }
    }


class DisciplineTypeRead(DisciplineTypeBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class DisciplineTypeReadPublic(DisciplineTypeRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(DisciplineTypeRead),
            ],
        }
    }


class CategoryBase(BaseSchema):
    id: int
    sex: int
    description: str
    short_description: str
    description_en: str
    short_description_en: str
    age: str
    deleted_at: Optional[AwareDatetime]


class CategoryCreate(CategoryBase):
    pass


class CategoryCreatePublic(CategoryCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(CategoryCreate),
            ],
        }
    }


class CategoryUpdate(CategoryBase):
    updated_at: AwareDatetime


class CategoryUpdatePublic(CategoryUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(CategoryUpdate),
            ],
        }
    }


class CategoryRead(CategoryBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class CategoryReadPublic(CategoryRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(CategoryRead),
            ],
        }
    }


class MeetBase(BaseSchema):
    id: UUID1
    type: str
    external_id: Optional[str]  # e.g., for external systems integration
    name: str
    start_at: AwareDatetime
    end_at: AwareDatetime
    registration_start_at: Optional[AwareDatetime]
    registration_end_at: Optional[AwareDatetime]
    registration_limit: Optional[int]  # 0 or 1 if there is some limit (eg team matches)
    location: str
    organizer: str
    deleted_at: Optional[AwareDatetime]


class MeetCreate(MeetBase):
    pass


class MeetCreatePublic(MeetCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(MeetCreate),
            ],
        }
    }


class MeetUpdate(MeetBase):
    updated_at: AwareDatetime


class MeetUpdatePublic(MeetUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(MeetUpdate),
            ],
        }
    }


class MeetRead(MeetBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class MeetReadPublic(MeetRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(MeetRead),
            ],
        }
    }


class MeetEventBase(BaseSchema):
    id: UUID1
    meet_id: UUID1
    discipline_id: int
    category_id: int
    start_at: AwareDatetime
    phase: str
    count: Optional[int]  # Total number of athletes in the event
    deleted_at: Optional[AwareDatetime]


class MeetEventCreate(MeetEventBase):
    pass


class MeetEventCreatePublic(MeetEventCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(MeetEventCreate),
            ],
        }
    }


class MeetEventUpdate(MeetEventBase):
    updated_at: AwareDatetime


class MeetEventUpdatePublic(MeetEventUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(MeetEventUpdate),
            ],
        }
    }


class MeetEventRead(MeetEventBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class MeetEventReadPublic(MeetEventRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(MeetEventRead),
            ],
        }
    }
