# ~/Soap/mongo_cleaner.py

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
MAX_QUOTA_MB = 512
TRIM_AT_MB = 450

def get_total_storage_used(fs_files):
    total = 0
    for doc in fs_files.find():
        total += doc.get("length", 0)
    return total / (1024 * 1024)  # Convert to MB

def purge_oldest_files():
    client = MongoClient(MONGO_URI)
    db = client["sop_backup"]
    fs_files = db["fs.files"]
    fs_chunks = db["fs.chunks"]

    total_used = get_total_storage_used(fs_files)

    if total_used < TRIM_AT_MB:
        print(f"✅ MongoDB usage {total_used:.2f}MB is under {TRIM_AT_MB}MB. No purge needed.")
        return

    print(f"⚠️ MongoDB usage {total_used:.2f}MB exceeds {TRIM_AT_MB}MB. Starting cleanup...")

    sorted_files = fs_files.find().sort("uploadDate", 1)  # Oldest first
    for doc in sorted_files:
        _id = doc["_id"]
        fs_chunks.delete_many({"files_id": _id})
        fs_files.delete_one({"_id": _id})
        print(f"🗑️ Deleted file: {doc['filename']} ({doc['length']} bytes)")
        total_used -= doc.get("length", 0) / (1024 * 1024)
        if total_used < TRIM_AT_MB:
            break

    print(f"✅ Cleanup complete. MongoDB usage is now below {TRIM_AT_MB}MB.")

if __name__ == "__main__":
    purge_oldest_files()
