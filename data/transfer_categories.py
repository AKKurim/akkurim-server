from datetime import datetime, timezone

import requests
from list_of_categories import CATEGORIES

url = "https://devapi.akkurim.cz/v1/sync/category"
all_categories = []
for category in CATEGORIES:
    data = {
        "id": category["Id"],
        "description": category["Description"],
        "short_description": category["ShortDescription"],
        "description_en": category["DescriptionEn"],
        "short_description_en": category["ShortDescriptionEn"],
        "sex": category["Sex"],
        "created_at": datetime.utcnow().isoformat() + "+00:00",
        "updated_at": datetime.utcnow().isoformat() + "+00:00",
        "deleted_at": None,
    }
    all_categories.append(data)

response = requests.post(
    url, json={"data": all_categories, "primary_keys": ["id"], "table": "category"}
)
print(response.status_code)
print(response.text)
