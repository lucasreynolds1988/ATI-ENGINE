# ~/Soap/auto_compression_reporter.py

import os
import gzip
import json
from datetime import datetime

LOG_FILE = os.path.expanduser("~/Soap/logs/relay_log.json")
REPORT_FILE = os.path.expanduser("~/Soap/logs/compression_report.json")

print("📊 Generating compression ratio report...")

if not os.path.exists(LOG_FILE):
    print("❌ Log file not found. No data to analyze.")
    exit(1)

with open(LOG_FILE, 'r') as f:
    entries = json.load(f)

report = []

def get_file_size(path):
    try:
        return os.path.getsize(path)
    except:
        return None

for entry in entries:
    gz_path = entry.get("path")
    if not gz_path or not os.path.exists(gz_path):
        continue

    with gzip.open(gz_path, 'rb') as f:
        raw_data = f.read()

    original_size = len(raw_data)
    compressed_size = get_file_size(gz_path)
    if compressed_size is None:
        continue

    ratio = round((1 - (compressed_size / original_size)) * 100, 2)
    report.append({
        "sha": entry.get("sha"),
        "timestamp": entry.get("timestamp"),
        "cloud": entry.get("cloud"),
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": ratio
    })

with open(REPORT_FILE, 'w') as f:
    json.dump(report, f, indent=2)

print(f"✅ Report complete: {REPORT_FILE} | Entries analyzed: {len(report)}")
