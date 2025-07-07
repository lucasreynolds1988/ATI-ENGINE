import os
from pymongo import MongoClient
from core.rotor_overlay import log_event

MONGO_URI = "mongodb+srv://lucasreynolds1988:Ruko0610%21%21@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
RESTORE_DIR = os.path.expanduser("~/Soap/overlay")

def restore_from_mongo(filename):
    client = MongoClient(MONGO_URI)
    db = client['fusion']
    col = db['files']
    docs = list(col.find({"filename": {"$regex": f"^{filename}(\\.part\\d+)?$"}}).sort("filename"))
    if not docs:
        log_event(f"Restore: No files found for {filename}")
        return
    with open(os.path.join(RESTORE_DIR, filename), 'wb') as f:
        for doc in docs:
            f.write(doc['data'])
    log_event(f"Restore: {filename} restored from MongoDB in {len(docs)} part(s)")

def verify_gcs_file_integrity(file_path):
    # Placeholder for real SHA verification logic
    log_event(f"Verified integrity for {os.path.basename(file_path)} (stub).")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        restore_from_mongo(sys.argv[1])
