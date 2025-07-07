#!/usr/bin/env python3
import os
from pymongo import MongoClient
import time

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def clean_old_manuals(days=30):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    cutoff = time.time() - (days * 86400)
    result = db["manuals"].delete_many({
        "approved": False,
        "upload_time": {"$lt": cutoff}
    })
    print(f"Deleted {result.deleted_count} unapproved manuals older than {days} days.")

if __name__ == "__main__":
    clean_old_manuals()
