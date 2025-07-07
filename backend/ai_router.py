#!/usr/bin/env python3
import os
import openai
import requests

OPENAI_KEY = os.getenv("OPENAI_API_KEY") or open("/home/lucasreynolds1988/Soap/secrets/openai.key").read().strip()
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or open("/home/lucasreynolds1988/Soap/secrets/gemini.key").read().strip()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

def ask_openai(prompt):
    openai.api_key = OPENAI_KEY
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return response.choices[0].message.content

def ask_gemini(prompt):
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Authorization": f"Bearer {GEMINI_KEY}"}
    json_data = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    r = requests.post(endpoint, headers=headers, json=json_data)
    return r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

def ask_ollama(prompt):
    r = requests.post(OLLAMA_URL, json={"model": "llama3", "prompt": prompt})
    return r.json().get("response", "")

def ask_any(prompt, engine="openai"):
    if engine == "openai":
        return ask_openai(prompt)
    elif engine == "gemini":
        return ask_gemini(prompt)
    elif engine == "ollama":
        return ask_ollama(prompt)
