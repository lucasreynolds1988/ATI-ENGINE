# ~/Soap/utils/mongo_chunker.py

import os
import time
from pymongo import MongoClient
from bson import Binary

# Constants
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net"
DB_NAME = "fusion"
COLLECTION_NAME = "files"
CHUNK_SIZE = 13 * 1024 * 1024  # 13MB max per BSON document

def upload_file_in_chunks(file_path):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    print(f"🔗 Uploading: {file_name} ({file_size / 1024 / 1024:.2f} MB)")

    with open(file_path, "rb") as f:
        chunk_index = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            document = {
                "file_name": file_name,
                "chunk_index": chunk_index,
                "chunk_data": Binary(chunk),
                "timestamp": time.time()
            }

            collection.insert_one(document)
            print(f"✅ Chunk {chunk_index} uploaded ({len(chunk)} bytes)")
            chunk_index += 1

    print("🎉 Upload complete!")

if __name__ == "__main__":
    test_file = input("📂 Enter file path to upload (chunked): ").strip()
    if os.path.exists(test_file):
        upload_file_in_chunks(test_file)
    else:
        print("❌ File not found.")
