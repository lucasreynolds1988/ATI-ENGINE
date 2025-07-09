# ~/Soap/core/mongo_safe_upload_v2.py

import os
import base64
import json
import pymongo
from core.rotor_overlay import log_event

MAX_SIZE_MB = 13
BASE = os.path.expanduser("~/Soap")
MANIFEST_PATH = os.path.join(BASE, "overlay/manifest.json")
PROTECTED_DIRS = ["core", "agents", "overlay", "eyes", "rotors", "wraps", "triggers"]

def load_manifest_paths():
    if not os.path.exists(MANIFEST_PATH):
        return []
    with open(MANIFEST_PATH, "r") as f:
        return [os.path.expanduser(entry["path"]) for entry in json.load(f)]

def upload_file_to_mongo(file_path, mongo_uri, db_name, collection_name):
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    file_size = os.path.getsize(file_path)
    if file_size > MAX_SIZE_MB * 1024 * 1024:
        log_event(f"[MONGO] ⚠️ Skipped too large: {file_path}")
        return

    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    record = {
        "filename": os.path.basename(file_path),
        "data": encoded
    }

    try:
        collection.insert_one(record)
        log_event(f"[MONGO] ✅ Uploaded: {file_path}")

        protected = load_manifest_paths()
        if not any(p in file_path for p in PROTECTED_DIRS) and file_path not in protected:
            os.remove(file_path)
            log_event(f"[MONGO] 🧼 Deleted local copy: {file_path}")

    except Exception as e:
        log_event(f"[MONGO] ❌ Upload failed: {str(e)}")
