#!/usr/bin/env python3
import os
from pymongo import MongoClient

# Updated MongoDB URI with new password
MONGO_URI = "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
SECRETS_DIR = os.path.expanduser("~/Soap/secrets")

def fetch_all_secrets():
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["secrets"]
    os.makedirs(SECRETS_DIR, exist_ok=True)
    for doc in col.find():
        path = os.path.join(SECRETS_DIR, doc['name'])
        with open(path, "wb") as f:
            f.write(doc['data'])
        print(f"Pulled secret {doc['name']} to {path}")

if __name__ == "__main__":
    fetch_all_secrets()
