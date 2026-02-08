from uuid import UUID

from app.models.group import GroupBase


class GroupCreateUpdate(GroupBase):
    trainer_ids: list[UUID]
    athlete_ids: list[UUID]


class PersonSimple:
    id: UUID
    first_name: str
    last_name: str


class GroupReadDetail(GroupBase):
    id: UUID
    trainers: list[PersonSimple]
    athletes: list[PersonSimple]

    model_config = {"arbitrary_types_allowed": True}
