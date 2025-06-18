import json

with open('config/responses.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    #print(data.get("intents", []))

cc = {intent['name'].lower(): intent for intent in data.get("intents", [])}
print(cc)