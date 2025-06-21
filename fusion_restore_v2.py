# ~/Soap/fusion_restore_v2.py

import os
import sys
import json
import hashlib
from pymongo import MongoClient
import bson

RESTORE_DIR = os.path.expanduser("~/Soap_overlay")
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
DB_NAME = "fusion"
COLLECTION_NAME = "files"

def compute_sha256(data):
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()

def restore_file(filename):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        chunks = list(collection.find({"filename": filename}))
        if not chunks:
            print(f"❌ No chunks found for: {filename}")
            return

        chunks.sort(key=lambda x: x["chunk_index"])
        data = b"".join(chunk["data"] for chunk in chunks)

        save_path = os.path.join(RESTORE_DIR, filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(data)

        sha = compute_sha256(data)
        print(f"✅ Restored: {filename} [SHA256: {sha}]")

    except Exception as e:
        print(f"❌ Error restoring {filename}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fusion_restore_v2.py <filename | manifest.json>")
        sys.exit(1)

    target = sys.argv[1]

    if target.endswith(".json"):
        try:
            with open(target, "r") as f:
                manifest = json.load(f)
            file_list = manifest.get("files", [])
            if not file_list:
                print(f"❌ Manifest is empty: {target}")
                sys.exit(1)
            for fname in file_list:
                restore_file(fname)
        except Exception as e:
            print(f"❌ Failed to process manifest {target}: {e}")
            sys.exit(1)
    else:
        restore_file(target)

if __name__ == "__main__":
    main()
