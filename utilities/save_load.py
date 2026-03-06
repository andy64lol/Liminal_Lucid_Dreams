import os
import sys
import json

SAVE_DIR = "data/saves"
MAX_SLOTS = 5

def get_save_paths():
    return [os.path.join(SAVE_DIR, f"save_{i}.json") for i in range(1, MAX_SLOTS + 1)]

def load_save(slot):
    save_path = get_save_paths()[slot - 1]
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            return json.load(f)
    else:
        return None

def save_game(slot, data):
    save_path = get_save_paths()[slot - 1]
    with open(save_path, "w") as f:
        json.dump(data, f)