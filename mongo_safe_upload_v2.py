#!/usr/bin/env python3
import os
from pymongo import MongoClient
import gridfs

class MongoChunker:
    def __init__(self, mongo_uri, database_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[database_name]
        self.fs = gridfs.GridFS(self.db)

    def upload_file(self, filepath):
        filename = os.path.basename(filepath)
        with open(filepath, 'rb') as file:
            data = file.read()
            existing = self.db.fs.files.find_one({"filename": filename})
            if existing:
                self.fs.delete(existing['_id'])
            self.fs.put(data, filename=filename)
            print(f"[INFO] ✅ Uploaded {filename} to MongoDB.")

    def upload_directory(self, upload_dir):
        for root, dirs, files in os.walk(upload_dir):
            for file in files:
                full_path = os.path.join(root, file)
                self.upload_file(full_path)

if __name__ == "__main__":
    import sys
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = "ati_oracle_engine"
    UPLOAD_DIR = sys.argv[sys.argv.index('--upload-dir') + 1]
    chunker = MongoChunker(MONGO_URI, DATABASE_NAME)
    chunker.upload_directory(UPLOAD_DIR)
