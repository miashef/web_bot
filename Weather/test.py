import json

with open("dump.json", 'r') as file:
    data = json.load(file)

with open('dump1234.json', 'w', encoding="utf-8") as file:
    json.dump(data['forecasts'][1], file, indent=3, ensure_ascii=False)
