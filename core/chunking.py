#!/usr/bin/env python3

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks for embeddings."""
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = tokens[i:i+chunk_size]
        chunks.append(' '.join(chunk))
        i += chunk_size - overlap
    return chunks
