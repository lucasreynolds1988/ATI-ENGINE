# ~/Soap/mongo_safe_upload_v2.py

import sys, os, bson
from pathlib import Path
from pymongo import MongoClient

MAX_SIZE = 13 * 1024 * 1024
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
client = MongoClient(MONGO_URI)
db = client["fusion"]
coll = db["files"]

def upload(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return

    data = path.read_bytes()
    for i in range(0, len(data), MAX_SIZE):
        chunk = data[i:i+MAX_SIZE]
        doc = {
            "filename": path.name,
            "chunk": i // MAX_SIZE,
            "data": bson.Binary(chunk)
        }
        coll.insert_one(doc)
        print(f"✅ Uploaded chunk {doc['chunk']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mongo_safe_upload_v2.py [file]")
    else:
        upload(sys.argv[1])
