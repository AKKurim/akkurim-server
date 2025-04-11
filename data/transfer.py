import uuid

import pandas as pd
import requests

athlete_status_id = "5f0e92e2-d123-11ef-9cd2-0242ac120002"  # active
club_id = "kurim"
url = "https://devapi.akkurim.cz/v1/athlete"


file = pd.ExcelFile("./data/prehled_clenu_09042025.xlsx")
# skip first 1 row
df = file.parse("Prehled clenu", skiprows=1)
count = 0
for row in df.iterrows():
    data = {
        "athlete_status_id": athlete_status_id,
        "birth_number": row[1]["RČ"].replace("/", ""),
        "city": row[1]["Město"],
        "club_id": "kurim",
        "ean": str(row[1]["EAN"]),
        "email": row[1]["E-mail"] if row[1]["E-mail"] != "" else None,
        "first_name": row[1]["Jméno"],
        "id": str(uuid.uuid1()),
        "last_name": row[1]["Příjmení"],
        "note": None,
        "phone": str(row[1]["Telefon"]) if row[1]["Telefon"] != "" else None,
        "profile_picture": None,
        "street": str(row[1]["Ulice + čp"]),
        "zip": str(row[1]["PSČ"]),
        "deleted_at": None,
    }
    for key, value in data.items():
        if value == "nan" or issubclass(float, type(value)):
            data[key] = None
    try:
        res = requests.post(url, json=data)
    except Exception as e:
        print(e)
        print(repr(data))
        print(type(data["email"]))
        print(data["email"] is float)
        break
    print(res.text)
