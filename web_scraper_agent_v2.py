# ~/Soap/web_scraper_agent_v2.py

import os
import sys
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path

BASE_DIR = Path.home() / "Soap/data/web_scrape"
VISITED_LOG = BASE_DIR / "visited_urls.txt"
SCRAPER_LOG = BASE_DIR / "scraper.log"
MAX_DEPTH = 10
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".jpeg", ".jpg", ".png", ".txt", ".html"]

os.makedirs(BASE_DIR, exist_ok=True)
visited = set()

if VISITED_LOG.exists():
    with open(VISITED_LOG, "r") as f:
        visited.update(line.strip() for line in f)

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(SCRAPER_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def save_file(content, url):
    sha = hashlib.sha256(url.encode()).hexdigest()
    ext = os.path.splitext(urlparse(url).path)[1] or ".html"
    if ext not in ALLOWED_EXTENSIONS and not url.endswith("/"):
        return
    filename = BASE_DIR / f"{sha}{ext}"
    with open(filename, "wb") as f:
        f.write(content)
    log(f"Saved {url} -> {filename.name}")

def crawl(url, depth=0):
    if depth > MAX_DEPTH or url in visited:
        return
    visited.add(url)
    with open(VISITED_LOG, "a") as f:
        f.write(url + "\n")

    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            log(f"Failed to load {url} (code {res.status_code})")
            return
        content_type = res.headers.get("Content-Type", "")
        save_file(res.content, url)

        if "text/html" in content_type:
            soup = BeautifulSoup(res.text, "html.parser")
            for link_tag in soup.find_all("a", href=True):
                next_url = urljoin(url, link_tag['href'])
                if urlparse(next_url).netloc == urlparse(url).netloc:
                    crawl(next_url, depth + 1)
    except Exception as e:
        log(f"Error on {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python3 web_scraper_agent_v2.py <URL>")
        sys.exit(1)
    root_url = sys.argv[1]
    log(f"🌐 Starting crawl: {root_url}")
    crawl(root_url)
    log("✅ Crawl complete.")
