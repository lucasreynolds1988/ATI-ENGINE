# ~/Soap/rotor_mongo.py

import time
import json
from pathlib import Path
from datetime import datetime
from pymongo import MongoClient

UPLOAD_PATH = Path.home() / "Soap/upload"
LOG_PATH = Path.home() / "Soap/logs/rotor_mongo.log"

client = MongoClient("mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
db = client["rotor"]
collection = db["ingest"]

def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

def insert_new_jsons():
    for file in UPLOAD_PATH.glob("*.json"):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                collection.insert_one(data)
            log(f"✅ Inserted: {file.name}")
            file.unlink()
        except Exception as e:
            log(f"❌ Failed insert: {file.name} - {e}")

def main():
    while True:
        insert_new_jsons()
        time.sleep(4)

if __name__ == "__main__":
    main()
