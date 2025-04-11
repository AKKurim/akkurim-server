from typing import Optional

from pydantic import UUID1, AfterValidator, AwareDatetime, EmailStr

from app.core.shared.base_schema import BaseSchema, generate_example_values


class ItemBase(BaseSchema):
    id: UUID1
    count: int
    name: str
    description: Optional[str]
    image: Optional[str]
    item_type_id: UUID1
    athlete_id: Optional[UUID1]
    deleted_at: Optional[AwareDatetime]


class ItemCreate(ItemBase):
    pass


class ItemCreatePublic(ItemCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ItemCreate),
            ],
        }
    }


class ItemUpdate(ItemBase):
    updated_at: AwareDatetime


class ItemUpdatePublic(ItemUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ItemUpdate),
            ],
        }
    }


class ItemRead(ItemBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class ItemReadPublic(ItemRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ItemRead),
            ],
        }
    }


class ItemTypeBase(BaseSchema):
    id: UUID1
    name: str
    deleted_at: Optional[AwareDatetime]


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemTypeCreatePublic(ItemTypeCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ItemTypeCreate),
            ],
        }
    }


class ItemTypeUpdate(ItemTypeBase):
    updated_at: AwareDatetime


class ItemTypeUpdatePublic(ItemTypeUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ItemTypeUpdate),
            ],
        }
    }


class ItemTypeRead(ItemTypeBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class ItemTypeReadPublic(ItemTypeRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(ItemTypeRead),
            ],
        }
    }
