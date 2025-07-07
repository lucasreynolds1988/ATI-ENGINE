import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from core.rotor_overlay import log_event
import os

visited = set()

def run_scraper(start_url, depth=1):
    found_urls = []

    def crawl(url, level):
        if url in visited or level > depth:
            return
        visited.add(url)
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            log_event(f"Scraper: Visited {url}")
            found_urls.append(url)

            for link in soup.find_all("a", href=True):
                href = link['href']
                full_url = urljoin(url, href)
                if full_url.startswith(start_url):
                    crawl(full_url, level + 1)
        except Exception as e:
            log_event(f"Scraper error: {e}")

    crawl(start_url, 0)
    return {"visited": list(visited), "total": len(visited)}
