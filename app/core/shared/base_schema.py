from datetime import datetime, timezone
from typing import Any

from pydantic import UUID1, AwareDatetime, BaseModel, EmailStr


# used for global configuration
class BaseSchema(BaseModel):
    pass


def generate_example_values(schema: BaseSchema) -> dict[str, Any]:
    example_values = {}
    for field_name, info in schema.model_fields.items():
        if info.annotation == AwareDatetime:
            example_values[field_name] = datetime.now(tz=timezone.utc).isoformat()
        else:
            if "id" in field_name:
                example_values[field_name] = "5f0e92e2-d123-11ef-9cd2-0242ac120002"
            elif field_name == "email":
                example_values[field_name] = "pepicek@gmail.com"
            elif field_name == "birth_number":
                example_values[field_name] = "7303102961"
            elif "first_name" in field_name:
                example_values[field_name] = "Pepa"
            elif "last_name" in field_name:
                example_values[field_name] = "Novák"
            elif "street" in field_name:
                example_values[field_name] = "Ulice 9"
            elif "city" in field_name:
                example_values[field_name] = "Praha"
            elif "zip" in field_name:
                example_values[field_name] = "11000"
            elif "phone" in field_name:
                example_values[field_name] = "00420123456789"
            elif "note" in field_name:
                example_values[field_name] = "Poznámka"
            elif "salary" in field_name:
                example_values[field_name] = 150
            elif "deleted_at" in field_name:
                example_values[field_name] = None
            else:
                example_values[field_name] = "some value"

    return example_values
