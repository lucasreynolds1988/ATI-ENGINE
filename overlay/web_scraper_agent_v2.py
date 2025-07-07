# ~/Soap/web_scraper_agent_v2.py

"""
Deep Recursive Web Scraper — Crawls target site, extracts docs, routes through rotor
"""

import os
import sys
import time
import json
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path

ROOT_DIR     = Path.home() / "Soap"
SCRAPE_LOG   = ROOT_DIR / "logs" / "scavenger.log"
VISITED_PATH = ROOT_DIR / "data" / "visited_urls.json"
SAVE_DIR     = ROOT_DIR / "web_scrape"
ROTOR_QUEUE  = ROOT_DIR / "rotor_queue"
MAX_DEPTH    = 5
SESSION_LIMIT = 10 * 1024 * 1024 * 1024  # 10GB max

for d in [SAVE_DIR, ROTOR_QUEUE, SCRAPE_LOG.parent, VISITED_PATH.parent]:
    d.mkdir(parents=True, exist_ok=True)

visited = set()
if VISITED_PATH.exists():
    try:
        with open(VISITED_PATH) as f:
            visited = set(json.load(f))
    except:
        visited = set()

downloaded_bytes = 0

def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()[:12]

def save_file(content, filename):
    global downloaded_bytes
    if downloaded_bytes + len(content) > SESSION_LIMIT:
        with open(SCRAPE_LOG, "a") as log:
            log.write(f"[{time.ctime()}] ⚠️ Session limit reached. Skipping {filename}\n")
        return None

    path = SAVE_DIR / filename
    with open(path, "wb") as f:
        f.write(content)
    downloaded_bytes += len(content)

    rotor_path = ROTOR_QUEUE / filename
    path.rename(rotor_path)
    return rotor_path

def crawl(url, depth=0):
    if depth > MAX_DEPTH or url in visited:
        return
    visited.add(url)

    try:
        res = requests.get(url, timeout=10)
        if "text/html" not in res.headers.get("Content-Type", ""):
            return
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("a", href=True)

        for tag in links:
            href = tag["href"]
            abs_url = urljoin(url, href)
            parsed = urlparse(abs_url)
            if not parsed.scheme.startswith("http"):
                continue

            if abs_url.endswith((".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".png")):
                try:
                    doc = requests.get(abs_url, timeout=10)
                    if doc.status_code == 200:
                        fname = f"{hash_url(abs_url)}_{os.path.basename(parsed.path)}"
                        path = save_file(doc.content, fname)
                        if path:
                            with open(SCRAPE_LOG, "a") as log:
                                log.write(f"[{time.ctime()}] 📄 Saved: {abs_url} → {path.name}\n")
                except Exception as e:
                    with open(SCRAPE_LOG, "a") as log:
                        log.write(f"[{time.ctime()}] ❌ Download failed: {abs_url} — {str(e)}\n")
            else:
                crawl(abs_url, depth + 1)
                time.sleep(0.75)  # pacing

    except Exception as e:
        with open(SCRAPE_LOG, "a") as log:
            log.write(f"[{time.ctime()}] ❌ Crawl error: {url} — {str(e)}\n")

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python3 web_scraper_agent_v2.py <url>")
        return
    start_url = sys.argv[1]
    crawl(start_url)

    with open(VISITED_PATH, "w") as f:
        json.dump(list(visited), f)

if __name__ == "__main__":
    main()
