#!/usr/bin/env python3
import os
import time
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def submit_feedback(user, manual_id, chunk_index, feedback, approved=False):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["feedback"]
    col.insert_one({
        "user": user,
        "manual_id": manual_id,
        "chunk_index": chunk_index,
        "feedback": feedback,
        "approved": approved,
        "timestamp": time.time()
    })
