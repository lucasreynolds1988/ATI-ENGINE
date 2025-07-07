#!/usr/bin/env python3
import os

def get_openai_key():
    return os.getenv("OPENAI_API_KEY") or open("/home/lucasreynolds1988/Soap/secrets/openai.key").read().strip()

def get_gemini_key():
    return os.getenv("GEMINI_API_KEY") or open("/home/lucasreynolds1988/Soap/secrets/gemini.key").read().strip()

def get_mongo_uri():
    return os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Jenco610##@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
