#!/usr/bin/env python3
import os
import uuid
import time
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def log_job(job_type, details, status="running"):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["jobs"]
    job_id = str(uuid.uuid4())
    col.insert_one({
        "job_id": job_id,
        "job_type": job_type,
        "details": details,
        "status": status,
        "timestamp": time.time()
    })
    return job_id

def update_job_status(job_id, status):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["jobs"]
    col.update_one({"job_id": job_id}, {"$set": {"status": status, "completed": time.time()}})
