#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rotor_overlay import log_event
from pymongo import MongoClient
import gridfs

MONGO_URI = os.getenv('MONGO_URI')
UPLOAD_DIR = sys.argv[sys.argv.index('--upload-dir') + 1]

def upload_to_mongo(upload_dir):
    client = MongoClient(MONGO_URI)
    db = client["ati_oracle_engine"]
    fs = gridfs.GridFS(db)

    for filename in os.listdir(upload_dir):
        filepath = os.path.join(upload_dir, filename)

        if os.path.isdir(filepath):
            print(f"[INFO] 📂 Skipping directory: {filepath}")
            continue  # explicitly skip directories

        with open(filepath, 'rb') as file:
            data = file.read()

            existing = db.fs.files.find_one({"filename": filename})
            if existing:
                fs.delete(existing['_id'])

            fs.put(data, filename=filename)
            print(f"[INFO] ✅ Uploaded {filename} to MongoDB.")
            log_event(f"Uploaded {filename} to MongoDB.")

if __name__ == "__main__":
    upload_to_mongo(UPLOAD_DIR)
