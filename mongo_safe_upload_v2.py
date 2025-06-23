# ~/Soap/mongo_safe_upload_v2.py

import os
import math
import time
import bson
from pathlib import Path
from pymongo import MongoClient
from rotor_overlay import log_event

MAX_CHUNK_SIZE = 13 * 1024 * 1024  # 13MB
UPLOAD_DIR = Path.home() / "Soap/uploads"
LOG_PATH = Path.home() / "Soap/logs/mongo_upload.log"

client = MongoClient("mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
db = client["fusion"]
collection = db["files"]

def chunk_and_upload(file_path):
    file_size = os.path.getsize(file_path)
    total_parts = math.ceil(file_size / MAX_CHUNK_SIZE)

    with open(file_path, "rb") as f:
        for part in range(total_parts):
            chunk = f.read(MAX_CHUNK_SIZE)
            doc = {
                "filename": file_path.name,
                "part": part,
                "total_parts": total_parts,
                "data": bson.Binary(chunk),
                "timestamp": time.time()
            }
            collection.insert_one(doc)
            log_event(f"📦 Uploaded {file_path.name} part {part+1}/{total_parts}", LOG_PATH)
            time.sleep(1)

def upload_all():
    for file in UPLOAD_DIR.glob("*"):
        if file.is_file():
            chunk_and_upload(file)

if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(LOG_PATH.parent, exist_ok=True)
    upload_all()
