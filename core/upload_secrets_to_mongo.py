#!/usr/bin/env python3
import os
from pymongo import MongoClient

# Updated MongoDB URI with new password
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Ruko0610%21%21@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
SECRETS_DIR = os.path.expanduser("~/Soap/secrets")

def upload_secret(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    name = os.path.basename(filename)
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["secrets"]
    col.replace_one({"name": name}, {"name": name, "data": data}, upsert=True)
    print(f"Uploaded {name} to MongoDB.")

if __name__ == "__main__":
    for fn in os.listdir(SECRETS_DIR):
        full_path = os.path.join(SECRETS_DIR, fn)
        if not os.path.isfile(full_path):
            continue
        upload_secret(full_path)
