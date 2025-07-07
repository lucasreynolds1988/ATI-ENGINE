#!/usr/bin/env python3
import os
import asyncio
from pymongo import MongoClient
import gridfs

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = "ati_oracle_engine"

class MongoChunker:
    def __init__(self, mongo_uri, database_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[database_name]
        self.fs = gridfs.GridFS(self.db)

    def restore_all_files(self, target_dir):
        os.makedirs(target_dir, exist_ok=True)
        for file in self.db.fs.files.find():
            data = self.fs.get(file['_id']).read()
            with open(os.path.join(target_dir, file['filename']), 'wb') as f:
                f.write(data)
            print(f"[INFO] ✅ Restored {file['filename']} from MongoDB.")

async def explicit_restore_cycle():
    chunker = MongoChunker(MONGO_URI, DATABASE_NAME)
    chunker.restore_all_files(target_dir="./overlay")
    print("[INFO] ✅ Explicit restore from MongoDB complete.")

def main():
    asyncio.run(explicit_restore_cycle())

if __name__ == "__main__":
    main()
