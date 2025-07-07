#!/usr/bin/env python3
from core.mongo_vectors import find_similar

def semantic_search(question, engine="openai", top_k=5, vector_func=None):
    if vector_func is None:
        from core.vectorizer import get_openai_vector, get_gemini_vector, get_ollama_vector
        vector_func = {
            "openai": get_openai_vector,
            "gemini": get_gemini_vector,
            "ollama": get_ollama_vector
        }[engine]
    query_vector = vector_func(question)
    return find_similar(engine, query_vector, top_k)
