#!/usr/bin/env python3
import openai
import requests

def check_openai():
    try:
        openai.Model.list()
        return True
    except Exception:
        return False

def check_gemini():
    try:
        # Simple GET for API status
        r = requests.get("https://generativelanguage.googleapis.com")
        return r.status_code == 200
    except Exception:
        return False

def check_ollama():
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except Exception:
        return False

def check_mongo():
    from pymongo import MongoClient
    try:
        client = MongoClient()
        client.server_info()
        return True
    except Exception:
        return False
