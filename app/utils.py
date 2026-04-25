import json

with open("data/nevup_seed_dataset.json", "r") as f:
    DATA = json.load(f)

def get_trader(user_id):
    for trader in DATA["traders"]:
        if trader["userId"] == user_id:
            return trader
    return None