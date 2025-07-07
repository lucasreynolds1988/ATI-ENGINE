#!/usr/bin/env python3
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymongo import MongoClient
from core.rotor_overlay import log_event

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Ruko0610%21%21@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
CHUNK_SIZE = 12 * 1024 * 1024  # 12MB per chunk

def mongo_safe_upload(file_path):
    client = MongoClient(MONGO_URI)
    db = client['fusion']
    col = db['files']
    file_size = os.path.getsize(file_path)
    basename = os.path.basename(file_path)

    if file_size <= CHUNK_SIZE:
        with open(file_path, 'rb') as f:
            content = f.read()
        col.insert_one({"filename": basename, "data": content})
        log_event(f"MongoDB: Uploaded {basename} ({file_size} bytes)")
    else:
        with open(file_path, 'rb') as f:
            idx = 0
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                partname = f"{basename}.part{idx:03d}"
                col.insert_one({"filename": partname, "data": chunk})
                log_event(f"MongoDB: Uploaded chunk {partname} ({len(chunk)} bytes)")
                idx += 1
        log_event(f"MongoDB: Finished uploading {basename} in {idx} chunks")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mongo_safe_upload(sys.argv[1])
