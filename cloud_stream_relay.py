# ~/Soap/cloud_stream_relay.py

import os
import time
import threading
import hashlib
import gzip
import json
from datetime import datetime
from pymongo import MongoClient
from bson.binary import Binary
import subprocess
from pathlib import Path

# === ROTOR CLOCK ===
class RotorClock:
    def __init__(self, interval=4):
        self.interval = interval
        self.last_tick = time.time()

    def wait_for_next(self):
        now = time.time()
        sleep_time = max(0, self.interval - (now - self.last_tick))
        time.sleep(sleep_time)
        self.last_tick = time.time()

# === CONFIG ===
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
DB = MongoClient(MONGO_URI).fusion
GCS_BUCKET = "gs://ati-rotor-fusion"
GITHUB_STAGING = Path.home() / "Soap/github_stream_staging"
LOG_PATH = Path.home() / "Soap/data/relay_log.json"
STATE_FILE = Path.home() / "Soap/relay_target_index.txt"

BUFFER_SIZE_LIMIT = 20  # lines per chunk
RELAY_TARGETS = ['MongoDB', 'GCS', 'GitHub']

# Ensure dirs
os.makedirs(GITHUB_STAGING, exist_ok=True)
os.makedirs(LOG_PATH.parent, exist_ok=True)

# === CORE STREAM BUFFER ===
buffer = []
buffer_lock = threading.Lock()
running = True

# Persistent target index
if STATE_FILE.exists():
    try:
        target_index = int(STATE_FILE.read_text().strip()) % len(RELAY_TARGETS)
    except:
        target_index = 0
else:
    target_index = 0

def sha256_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()

def log_transfer(info):
    entry = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "sha": info["sha"],
        "size": info["size"],
        "target": info["target"],
        "chunk_id": info["chunk_id"],
    }
    try:
        if LOG_PATH.exists():
            with open(LOG_PATH, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(LOG_PATH, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"⚠️ Log error: {e}")

def read_stream():
    print("🔁 [Input] Streaming input. Type #EOF to flush, #EXIT to stop.")
    while running:
        try:
            line = input()
        except EOFError:
            break
        with buffer_lock:
            buffer.append(line)
        if line.strip() == "#EXIT":
            print("🛑 [Input] Exiting stream input...")
            break

def upload_to_mongo(chunk_id, data_gz):
    DB.file_chunks.insert_one({
        "chunk_id": chunk_id,
        "data": Binary(data_gz),
        "origin": "relay.gz"
    })
    print(f"🛰️ Mongo pushed: {chunk_id}")

def upload_to_gcs(chunk_id, data_gz):
    tmp_path = f"/tmp/{chunk_id}.gz"
    with open(tmp_path, "wb") as f:
        f.write(data_gz)
    subprocess.run(f"gsutil cp {tmp_path} {GCS_BUCKET}/stream/{chunk_id}.gz", shell=True)
    os.remove(tmp_path)
    print(f"☁️ GCS pushed: {chunk_id}")

def upload_to_github(chunk_id, data_gz):
    filename = GITHUB_STAGING / f"{chunk_id}.gz"
    with open(filename, "wb") as f:
        f.write(data_gz)
    try:
        subprocess.run(["git", "-C", str(GITHUB_STAGING), "add", "."], check=True)
        subprocess.run(["git", "-C", str(GITHUB_STAGING), "commit", "-m", f"🧠 Stream relay: {chunk_id}"], check=True)
        subprocess.run(["git", "-C", str(GITHUB_STAGING), "push", "origin", "main"], check=True)
        print(f"🌐 GitHub pushed: {chunk_id}")
    except Exception as e:
        print(f"⚠️ GitHub error: {e}")

def rotor_push(clock):
    global target_index
    chunk_index = 0
    while running:
        clock.wait_for_next()
        with buffer_lock:
            if len(buffer) < BUFFER_SIZE_LIMIT and "#EOF" not in buffer:
                continue
            chunk_lines = []
            while buffer and len(chunk_lines) < BUFFER_SIZE_LIMIT:
                line = buffer.pop(0)
                if line.strip() == "#EOF":
                    break
                chunk_lines.append(line)

        if not chunk_lines:
            continue

        raw = "\n".join(chunk_lines).encode()
        data_gz = gzip.compress(raw)
        sha = sha256_bytes(data_gz)
        chunk_id = f"{sha[:12]}_{chunk_index}"
        target = RELAY_TARGETS[target_index]

        if target == "MongoDB":
            upload_to_mongo(chunk_id, data_gz)
        elif target == "GCS":
            upload_to_gcs(chunk_id, data_gz)
        elif target == "GitHub":
            upload_to_github(chunk_id, data_gz)

        log_transfer({
            "sha": sha,
            "size": len(data_gz),
            "target": target,
            "chunk_id": chunk_id
        })

        # ✅ Fix: rotate correctly and save the *next* index
        next_index = (target_index + 1) % len(RELAY_TARGETS)
        STATE_FILE.write_text(str(next_index))
        target_index = next_index
        chunk_index += 1

def rotor_pull_and_run():
    print("🔄 [Rotor] Checking remote stream...")
    doc = DB.file_chunks.find_one({"origin": "relay.gz"})
    if not doc:
        print("⚠️ No compressed chunks found.")
        return
    data = gzip.decompress(doc["data"])
    code = data.decode()
    if "#RUNTIME" in code:
        print("🚦 [EXEC] Running streamed payload...")
        exec(code, globals())
    else:
        print("📜 [RECV] Code received, no #RUNTIME found.")

def start_relay():
    clock = RotorClock()
    t1 = threading.Thread(target=read_stream)
    t2 = threading.Thread(target=rotor_push, args=(clock,))
    t3 = threading.Thread(target=rotor_pull_and_run)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    global running
    running = False
    t2.join()
    t3.join()

if __name__ == "__main__":
    start_relay()
