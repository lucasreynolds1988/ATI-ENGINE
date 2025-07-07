#!/usr/bin/env python3
import os
import time
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def record_manual_metadata(manual_id, filename, uploader, approved=False, notes=""):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["manuals"]
    col.update_one(
        {"manual_id": manual_id},
        {"$set": {
            "filename": filename,
            "uploader": uploader,
            "approved": approved,
            "notes": notes,
            "upload_time": time.time()
        }},
        upsert=True
    )
