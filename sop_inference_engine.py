# ~/Soap/sop_inference_engine.py

import os
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup
import re
import json
import datetime

SCRAPE_DIR = Path.home() / "Soap/data/web_scrape"
OUTPUT_DIR = Path.home() / "Soap/data/sop_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_html_text(html_bytes):
    try:
        soup = BeautifulSoup(html_bytes, "html.parser")
        text = soup.get_text(separator="\n")
        return text.strip()
    except Exception as e:
        print(f"❌ Failed to parse HTML: {e}")
        return ""

def extract_sections(text):
    sections = {
        "title": None,
        "purpose": None,
        "scope": None,
        "tools": [],
        "materials": [],
        "safety": [],
        "procedure": [],
        "troubleshooting": [],
        "maintenance": [],
        "references": []
    }

    lines = text.splitlines()
    section = "procedure"
    for line in lines:
        l = line.strip().lower()

        if "purpose" in l:
            section = "purpose"
        elif "scope" in l:
            section = "scope"
        elif "tool" in l:
            section = "tools"
        elif "material" in l:
            section = "materials"
        elif "safety" in l:
            section = "safety"
        elif "procedure" in l or "steps" in l:
            section = "procedure"
        elif "troubleshooting" in l:
            section = "troubleshooting"
        elif "maintenance" in l:
            section = "maintenance"
        elif "reference" in l:
            section = "references"

        if section in ["tools", "materials", "safety", "procedure", "troubleshooting", "maintenance", "references"]:
            sections[section].append(line.strip())
        elif section in ["purpose", "scope"] and not sections[section]:
            sections[section] = line.strip()

    return sections

def synthesize_sop(file_path):
    print(f"🧠 Processing: {file_path.name}")
    try:
        html_bytes = file_path.read_bytes()
        raw_text = clean_html_text(html_bytes)
        sop = extract_sections(raw_text)

        sop_meta = {
            "title": f"Auto-SOP from {file_path.name}",
            "version": "1.0",
            "status": "Gen
