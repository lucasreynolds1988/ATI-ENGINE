#!/usr/bin/env python3
import os
from pymongo import MongoClient
import json

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def export_vector_index(path="vector_index_export.json"):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["vectors"]
    with open(path, "w") as f:
        json.dump(list(col.find({}, {"_id": 0})), f)
    print(f"Exported vector index to {path}")

def import_vector_index(path="vector_index_export.json"):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["vectors"]
    with open(path, "r") as f:
        data = json.load(f)
    col.insert_many(data)
    print(f"Imported {len(data)} vectors from {path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_vector_index()
    else:
        export_vector_index()
