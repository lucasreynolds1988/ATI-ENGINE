#!/usr/bin/env python3
import os
from pymongo import MongoClient
import time

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def clean_old_jobs(days=30):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    cutoff = time.time() - (days * 86400)
    result = db["jobs"].delete_many({"timestamp": {"$lt": cutoff}})
    print(f"Deleted {result.deleted_count} jobs older than {days} days.")

if __name__ == "__main__":
    clean_old_jobs()
