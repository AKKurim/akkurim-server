import uuid

import pandas as pd
import requests

athlete_status_id = "5f0e92e2-d123-11ef-9cd2-0242ac120002"  # active
club_id = "kurim"
url = "https://devapi.akkurim.cz/v1/athlete"


file = pd.ExcelFile("./data/prehled_clenu_09042025.xlsx")
# skip first 1 row
df = file.parse("Prehled clenu", skiprows=1)
for row in df.iterrows():
    data = {
        "athlete_status_id": athlete_status_id,
        "birth_number": row[1]["RČ"].replace("/", ""),
        "city": row[1]["Město"],
        "club_id": "kurim",
        "ean": str(row[1]["EAN"]),
        "email": row[1]["E-mail"],
        "first_name": row[1]["Jméno"],
        "id": str(uuid.uuid1()),
        "last_name": row[1]["Příjmení"],
        "note": "",
        "phone": str(row[1]["Telefon"]),
        "profile_picture": "",
        "street": row[1]["Ulice + čp"],
        "zip": str(row[1]["PSČ"]),
    }
    print("requests")
    res = requests.post(url, json=data)
    print(res.text)
    break
