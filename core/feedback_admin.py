#!/usr/bin/env python3
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def list_feedback(approved=None):
    client = MongoClient(MONGO_URI)
    col = client["fusion"]["feedback"]
    query = {}
    if approved is not None:
        query["approved"] = approved
    return list(col.find(query, {"_id": 0}))

def approve_feedback(feedback_id):
    client = MongoClient(MONGO_URI)
    col = client["fusion"]["feedback"]
    col.update_one({"_id": feedback_id}, {"$set": {"approved": True}})
