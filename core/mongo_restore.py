#!/usr/bin/env python3
import os
from pymongo import MongoClient
import gridfs

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
DATABASE_NAME = "ati_oracle_engine"
RESTORE_DIR = os.path.expanduser("~/Soap/mongo_restore")

def mongo_restore():
    os.makedirs(RESTORE_DIR, exist_ok=True)
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    fs = gridfs.GridFS(db)
    print("Restoring all files from MongoDB GridFS...")
    for file in db.fs.files.find():
        filename = file['filename']
        with open(os.path.join(RESTORE_DIR, filename), 'wb') as f_out:
            f_out.write(fs.get(file['_id']).read())
        print(f"Restored: {filename}")

if __name__ == "__main__":
    mongo_restore()
