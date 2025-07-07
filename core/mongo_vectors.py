#!/usr/bin/env python3
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")

def store_chunk(manual_id, idx, chunk, vectors):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["vectors"]
    doc = {
        "manual_id": manual_id,
        "chunk_index": idx,
        "text": chunk,
        **vectors
    }
    col.insert_one(doc)

def find_similar(engine, query_vector, top_k=5):
    client = MongoClient(MONGO_URI)
    db = client["fusion"]
    col = db["vectors"]
    # Use naive dot-product for demo (replace with vector DB for prod)
    all_docs = list(col.find({f"{engine}_vector": {"$exists": True}}))
    def score(doc):
        v = doc.get(f"{engine}_vector", [])
        if not v or not query_vector: return -1
        return sum([a*b for a, b in zip(v, query_vector)])
    return sorted(all_docs, key=score, reverse=True)[:top_k]

