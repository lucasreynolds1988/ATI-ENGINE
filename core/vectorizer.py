#!/usr/bin/env python3
import os
import time
import requests
import openai

# Rotor timing: track last call time for each engine
last_call = {
    "openai": 0,
    "gemini": 0,
    "ollama": 0
}
MIN_INTERVAL = 4.0  # seconds

def rotor_wait(engine):
    now = time.time()
    elapsed = now - last_call[engine]
    if elapsed < MIN_INTERVAL:
        sleep_time = MIN_INTERVAL - elapsed
        print(f"[Rotor] Waiting {sleep_time:.2f} seconds before next {engine} call...")
        time.sleep(sleep_time)
    last_call[engine] = time.time()

OPENAI_KEY = os.getenv("OPENAI_API_KEY") or open("/home/lucasreynolds1988/Soap/secrets/openai.key").read().strip()
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or open("/home/lucasreynolds1988/Soap/secrets/gemini.key").read().strip()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/embeddings")

def get_openai_vector(text):
    rotor_wait("openai")
    openai.api_key = OPENAI_KEY
    response = openai.embeddings.create(model="text-embedding-ada-002", input=text)
    return response.data[0].embedding

def get_gemini_vector(text):
    rotor_wait("gemini")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedText"
    headers = {"Authorization": f"Bearer {GEMINI_KEY}"}
    json_data = {"content": text}
    r = requests.post(endpoint, headers=headers, json=json_data)
    return r.json().get("embedding", {}).get("values", [])

def get_ollama_vector(text):
    rotor_wait("ollama")
    r = requests.post(OLLAMA_URL, json={"model": "nomic-embed-text", "prompt": text})
    return r.json().get("embedding", [])

def vectorize_all(text):
    return {
        "openai_vector": get_openai_vector(text),
        "gemini_vector": get_gemini_vector(text),
        "ollama_vector": get_ollama_vector(text)
    }
