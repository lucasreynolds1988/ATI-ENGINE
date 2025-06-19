# ~/Soap/mongo_force_cleaner.py
import pymongo
from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
client = pymongo.MongoClient(MONGO_URI)
db = client["soap"]
fs_files = db["fs.files"]
fs_chunks = db["fs.chunks"]

# Force deletion count
limit = 100
deleted = 0

print(f"🧨 MongoDB Forced Cleaner Initiated — targeting {limit} oldest files...")

old_files = fs_files.find().sort("uploadDate", 1).limit(limit)
for file in old_files:
    file_id = file["_id"]
    fs_chunks.delete_many({"files_id": file_id})
    fs_files.delete_one({"_id": file_id})
    print(f"🗑️ Deleted: {file.get('filename', str(file_id))}")
    deleted += 1

print(f"✅ Cleanup Complete — {deleted} file(s) removed.")
