# ~/Soap/core/fusion_manifest.py

import os
import json

MANIFEST_PATH = os.path.expanduser("~/Soap/overlay/manifest.json")

def load_manifest_paths():
    if not os.path.exists(MANIFEST_PATH):
        return []
    with open(MANIFEST_PATH, "r") as f:
        return [os.path.expanduser(entry["path"]) for entry in json.load(f)]
