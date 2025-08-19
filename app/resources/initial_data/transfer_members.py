import uuid

import pandas as pd
import requests

club_id = "kurim"
url = "https://devapi.akkurim.cz/v1/athlete"
trainer_url = "https://devapi.akkurim.cz/v1/trainer"
guardian_url = "https://devapi.akkurim.cz/v1/guardian"

guardian_list = []

file = pd.ExcelFile("./app/resources/initial_data/prehled_clenu.xlsx")
# skip first 1 row
df = file.parse("Prehled clenu", skiprows=1)
count = 0
for row in df.iterrows():
    athl_id = str(uuid.uuid1())
    data = {
        "status": "active",
        "bank_number": None,
        "birth_number": row[1]["RČ"].replace("/", ""),
        "city": row[1]["Město"],
        "club_id": "kurim",
        "ean": str(row[1]["EAN"]),
        "email": row[1]["E-mail"] if row[1]["E-mail"] != "" else None,
        "first_name": row[1]["Jméno"],
        "id": str(athl_id),
        "last_name": row[1]["Příjmení"],
        "note": None,
        "phone": (
            str(int(row[1]["Telefon"]))
            if row[1]["Telefon"] != "" and type(row[1]["Telefon"]) is str
            else None
        ),
        "profile_image_id": None,
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

    if row[1]["Trenér třída"] != "" and type(row[1]["Trenér třída"]) is str:
        print("Adding trainer for athlete", row[1]["Jméno"], row[1]["Příjmení"])
        print("Trainer qualification:", row[1]["Trenér třída"])
        trainer_data = {
            "athlete_id": athl_id,
            "bank_number": None,
            "id": str(uuid.uuid1()),
            "qualification": row[1]["Trenér třída"],
            "salary_per_hour": 0,
            "status": "active",
            "deleted_at": None,
        }
        for key, value in data.items():
            if value == "nan" or issubclass(float, type(value)):
                data[key] = None
        res = requests.post(trainer_url, json=trainer_data)
        print(res.text)

    if row[1]["E-mail zákonného zástupce"] != "":
        # search in guardian_list for a same email
        for guardian in guardian_list:
            if guardian["email"] == row[1]["E-mail zákonného zástupce"]:
                guardian["athlete_ids"].append(athl_id)
                break
        guardian_data = {
            "athlete_ids": [athl_id],
            "bank_number": None,
            "email": row[1]["E-mail zákonného zástupce"],
            "first_name": "-",
            "id": str(uuid.uuid1()),
            "last_name": "-",
            "phone": (
                str(int(row[1]["Telefon"]))
                if row[1]["Telefon"] != "" and type(row[1]["Telefon"]) is str
                else None
            ),
            "deleted_at": None,
        }
        guardian_list.append(guardian_data)

for guardian in guardian_list:
    for key, value in guardian.items():
        if value == "nan" or issubclass(float, type(value)):
            guardian[key] = None
    for value in guardian["athlete_ids"]:
        url = guardian_url + f"/{value}"
        res = requests.post(url, json=guardian)
        print(res.text)
