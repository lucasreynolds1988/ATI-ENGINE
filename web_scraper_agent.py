# ~/Soap/web_scraper_agent_v2.py

import os
import sys
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path

SAVE_PATH = Path.home() / "Soap/data/web_scrape"
VISITED_LOG = SAVE_PATH / "visited_urls_v2.txt"
SESSION_CAP_MB = 10 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpeg", ".jpg", ".png", ".txt"}

seen_hashes = set()
downloaded_size = 0
visited = set()

SAVE_PATH.mkdir(parents=True, exist_ok=True)


def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()


def already_visited(url):
    return hash_url(url) in visited


def mark_visited(url):
    with open(VISITED_LOG, "a") as f:
        f.write(f"{hash_url(url)} | {url}\n")
    visited.add(hash_url(url))


def get_extension(url):
    parsed = urlparse(url)
    return os.path.splitext(parsed.path)[1].lower()


def is_file(url):
    return get_extension(url) in ALLOWED_EXTENSIONS


def download_file(url):
    global downloaded_size
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        file_hash = hashlib.sha256(r.content).hexdigest()
        if file_hash in seen_hashes:
            return

        seen_hashes.add(file_hash)
        size_kb = len(r.content) / 1024
        downloaded_size += size_kb / 1024

        if downloaded_size > SESSION_CAP_MB:
            print("❌ [Limit] 10GB session cap reached.")
            sys.exit(0)

        filename = SAVE_PATH / f"{file_hash}.bin"
        with open(filename, "wb") as f:
            f.write(r.content)
        print(f"📥 Saved: {filename.name} ({round(size_kb,1)}KB)")

    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")


def scrape(url, depth=0, max_depth=5):
    if depth > max_depth or already_visited(url):
        return

    print(f"🔍 Scanning: {url}")
    mark_visited(url)

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # save page text
        page_hash = hash_url(url)
        content_path = SAVE_PATH / f"{page_hash}.txt"
        with open(content_path, "w") as f:
            f.write(soup.get_text())

        # find links
        for link_tag in soup.find_all("a", href=True):
            href = link_tag["href"]
            full_url = urljoin(url, href)
            ext = get_extension(full_url)
            if is_file(full_url):
                download_file(full_url)
            elif urlparse(full_url).netloc == urlparse(url).netloc:
                scrape(full_url, depth + 1, max_depth)

    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 web_scraper_agent_v2.py <URL>")
        sys.exit(1)

    start_url = sys.argv[1]
    print("🚀 Starting AI Scavenger Mode (v2)...")
    scrape(start_url)
    print("✅ Complete: Rotor ready to compress")
