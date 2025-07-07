#!/usr/bin/env python3
import os
import uuid
from core.text_extract import extract_text
from core.chunking import chunk_text
from core.vectorizer import vectorize_all
from core.mongo_vectors import store_chunk

def process_manual(path):
    manual_id = str(uuid.uuid4())
    text = extract_text(path)
    chunks = chunk_text(text)
    for idx, chunk in enumerate(chunks):
        vectors = vectorize_all(chunk)
        store_chunk(manual_id, idx, chunk, vectors)
    print(f"Processed and stored vectors for manual {manual_id}")

if __name__ == "__main__":
    import sys
    process_manual(sys.argv[1])
