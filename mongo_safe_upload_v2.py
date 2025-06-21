# ~/Soap/mongo_safe_upload_v2.py

import os
import math
import bson
import time
from pymongo import MongoClient

MAX_CHUNK_SIZE = 13 * 1024 * 1024  # 13MB
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
DB_NAME = "fusion"
COLLECTION_NAME = "files"

def chunk_file(file_path):
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(MAX_CHUNK_SIZE)
            if not chunk:
                break
            yield chunk

def upload_in_chunks(file_path):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    coll = db[COLLECTION_NAME]

    file_name = os.path.basename(file_path)
    print(f"🔩 Preparing Mongo upload for: {file_name}")
    chunks = list(chunk_file(file_path))
    total = len(chunks)

    if total == 0:
        print("⚠️ Empty file.")
        return

    for i, chunk in enumerate(chunks):
        doc = {
            "filename": file_name,
            "chunk_index": i,
            "total_chunks": total,
            "data": bson.binary.Binary(chunk),
            "timestamp": time.time()
        }
        coll.insert_one(doc)
        print(f"✅ Uploaded chunk {i+1}/{total}")

    print(f"🎉 Mongo Upload Complete: {file_name} in {total} chunks")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 mongo_safe_upload_v2.py /path/to/large_file")
        exit(1)
    upload_in_chunks(sys.argv[1])
