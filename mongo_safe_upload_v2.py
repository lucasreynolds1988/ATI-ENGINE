# ~/Soap/mongo_safe_upload_v2.py

import os
import math
import time
import bson
from pymongo import MongoClient
from pathlib import Path

MAX_CHUNK_SIZE = 13 * 1024 * 1024  # 13MB
client = MongoClient("mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
db = client["fusion"]
coll = db["chunks"]

def safe_upload_to_mongo(file_path):
    try:
        file_path = Path(file_path)
        file_size = file_path.stat().st_size
        num_parts = math.ceil(file_size / MAX_CHUNK_SIZE)

        with open(file_path, "rb") as f:
            for i in range(num_parts):
                chunk_data = f.read(MAX_CHUNK_SIZE)
                doc = {
                    "filename": file_path.name,
                    "sha": get_sha256(file_path),
                    "part": i,
                    "total_parts": num_parts,
                    "data": bson.Binary(chunk_data),
                    "timestamp": time.time()
                }
                coll.insert_one(doc)
                print(f"📦 Uploaded part {i+1}/{num_parts} → MongoDB")

        return True
    except Exception as e:
        print(f"❌ MongoDB upload error: {e}")
        return False

def get_sha256(file_path):
    import hashlib
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

if __name__ == "__main__":
    path = input("Enter file path to upload: ").strip()
    if os.path.exists(path):
        safe_upload_to_mongo(path)
    else:
        print("❌ File not found.")
