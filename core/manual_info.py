#!/usr/bin/env python3
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def get_manual_info(manual_id):
    client = MongoClient(MONGO_URI)
    col = client["fusion"]["manuals"]
    return col.find_one({"manual_id": manual_id}, {"_id": 0})
