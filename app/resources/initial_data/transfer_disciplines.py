import requests
from list_of_disciplines import DISCIPLINES

url = "https://devapi.akkurim.cz/v1/discipline"
for discipline in DISCIPLINES:
    data = {
        "id": discipline["Id"],
        "description": discipline["Description"],
        "short_description": discipline["ShortDescription"],
        "description_en": discipline["DescriptionEn"],
        "short_description_en": discipline["ShortDescriptionEn"],
        "discipline_type_id": discipline["DisciplineType"],
        "deleted_at": None,
    }
    try:
        res = requests.post(url, json=data)
    except Exception as e:
        print(e)
        print(repr(data))
        break
    print(res.text)
