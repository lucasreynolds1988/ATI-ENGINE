#!/usr/bin/env python3
import os
from pymongo import MongoClient
import gridfs

MONGO_URI = os.getenv('MONGO_URI')
DOWNLOAD_DIR = os.path.expanduser('~/Soap')

def restore_all():
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    fs = gridfs.GridFS(db)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for grid_out in fs.find():
        file_path = os.path.join(DOWNLOAD_DIR, grid_out.filename)
        with open(file_path, 'wb') as f:
            f.write(grid_out.read())
            print(f"[INFO] Restored {grid_out.filename}")

if __name__ == "__main__":
    restore_all()
