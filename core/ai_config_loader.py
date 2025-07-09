# ~/Soap/core/ai_config_loader.py

import os
import json

CONFIG_PATH = os.path.expanduser("~/Soap/configs/ai_config.json")

def load_ai_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("AI config file not found.")
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
