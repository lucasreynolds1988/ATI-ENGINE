# ~/Soap/mongo_rotor.py

import os
import hashlib
import base64
import json
from pathlib import Path
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
DB_NAME = "fusion"
COLL_NAME = "files"
CHUNK_SIZE = 13 * 1024 * 1024
LOG_PATH = os.path.expanduser("~/Soap/.fusion-log.json")

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_log():
    return json.load(open(LOG_PATH)) if os.path.exists(LOG_PATH) else {}

def save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def safe_upload_to_mongo(file_path):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    coll = db[COLL_NAME]

    with open(file_path, "rb") as f:
        data = f.read()

    file_id = hashlib.sha1(data).hexdigest()
    chunks = [base64.b64encode(data[i:i+CHUNK_SIZE]).decode("utf-8")
              for i in range(0, len(data), CHUNK_SIZE)]

    for i, chunk in enumerate(chunks):
        coll.insert_one({
            "file_id": file_id,
            "filename": file_path.name,
            "path": str(file_path),
            "chunk_index": i,
            "chunk_data": chunk,
            "total_chunks": len(chunks)
        })

    print(f"✅ Mongo upload: {file_path.name} ({len(chunks)} chunks)")
    return True

def scan_and_upload():
    log = load_log()
    search_dirs = ["/home", "/root"]

    for base_dir in search_dirs:
        for dirpath, _, filenames in os.walk(base_dir):
            for file in filenames:
                full_path = Path(os.path.join(dirpath, file))
                try:
                    if not full_path.is_file(): continue
                    if full_path.name.startswith("."): continue

                    file_hash = sha256(full_path)
                    if file_hash in log: continue

                    success = safe_upload_to_mongo(full_path)
                    if success:
                        os.remove(full_path)
                        log[file_hash] = {
                            "path": str(full_path),
                            "dest": "mongo"
                        }
                        print(f"🧹 Deleted: {full_path}")
                except Exception as e:
                    print(f"⚠️ Error on {full_path}: {e}")

    save_log(log)

if __name__ == "__main__":
    scan_and_upload()
