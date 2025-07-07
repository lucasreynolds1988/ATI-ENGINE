#!/usr/bin/env python3
from core.vector_search import semantic_search
from core.ai_router import ask_any

def generate_sop(question, engine="openai", top_k=5):
    # Find relevant chunks
    matches = semantic_search(question, engine=engine, top_k=top_k)
    # Collate for LLM
    context = "\n\n".join([m["text"] for m in matches])
    prompt = f"You are an expert technician. Use these manual excerpts:\n\n{context}\n\nQ: {question}\nA:"
    return ask_any(prompt, engine=engine)
