# ~/Soap/delete_chunks.py

from pymongo import MongoClient
from bson import ObjectId

# MongoDB config
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
TARGET_ID = ObjectId("68537cba45f6d93ee7b9a26b")  # Chunks tied to backend_1750301860.tar.gz

def purge_chunks():
    client = MongoClient(MONGO_URI)
    db = client["sop_backup"]
    chunks = db["fs.chunks"]
    
    result = chunks.delete_many({"files_id": TARGET_ID})
    print(f"✅ Deleted {result.deleted_count} orphaned chunks for ObjectId {TARGET_ID}")

if __name__ == "__main__":
    purge_chunks()
