# ~/Soap/batch_stream_simulator.py

import os
import gzip
import hashlib
import random
import string
import time
import json
from datetime import datetime

# === CONFIG ===
TARGET_DIR = os.path.expanduser("~/Soap/data/relay_chunks")
LOG_FILE = os.path.expanduser("~/Soap/logs/relay_log.json")
CHUNK_COUNT = 20  # You can raise this for stress testing
DELAY_BETWEEN_CHUNKS = 2  # seconds
CLOUD_TARGETS = ["MongoDB", "GCS", "GitHub"]

os.makedirs(TARGET_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def generate_random_payload():
    header = f"# Generated Stream Chunk\n# Timestamp: {datetime.now().isoformat()}\n"
    body = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(200, 2000)))
    payload = header + body
    if random.random() < 0.2:
        payload += "\n#RUNTIME\nprint(\"Live execution from batch stream\")"
    return payload.encode("utf-8")

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def compress_data(data):
    compressed_path = os.path.join(TARGET_DIR, f"stream_{int(time.time()*1000)}.gz")
    with gzip.open(compressed_path, 'wb') as f:
        f.write(data)
    return compressed_path

def pick_random_cloud():
    return random.choice(CLOUD_TARGETS)

def append_to_log(entry):
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)
    with open(LOG_FILE, 'r+') as f:
        log = json.load(f)
        log.append(entry)
        f.seek(0)
        json.dump(log, f, indent=2)

# === MAIN LOOP ===
print(f"🚀 Starting batch stream simulation: {CHUNK_COUNT} chunks")
for i in range(CHUNK_COUNT):
    print(f"⏳ Generating chunk {i+1}/{CHUNK_COUNT}...")
    raw = generate_random_payload()
    sha = sha256(raw)
    compressed_path = compress_data(raw)
    cloud = pick_random_cloud()

    log_entry = {
        "sha": sha,
        "timestamp": datetime.now().isoformat(),
        "cloud": cloud,
        "path": compressed_path
    }
    append_to_log(log_entry)

    print(f"✅ Chunk {i+1} | SHA: {sha[:8]}... | Cloud: {cloud}")
    time.sleep(DELAY_BETWEEN_CHUNKS)

print("🎯 Batch stream simulation complete.")
