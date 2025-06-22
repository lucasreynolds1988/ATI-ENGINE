# ~/Soap/fusion_restore_v2.py

import os
import time
import subprocess
import logging
from pathlib import Path
from pymongo import MongoClient
import bson

# Constants
GITHUB_REPO = "https://github.com/lucasr610/Soap.git"
LOCAL_PATH = str(Path.home() / "Soap")
LOG_PATH = Path(LOCAL_PATH) / "logs/restore.log"
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net"
MAX_MONGO_CHUNK = 13 * 1024 * 1024  # 13MB
MONGO_DB = "rotor"
MONGO_COLLECTION = "fusion_chunks"

# Setup logging
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def log(msg): 
    print(msg)
    logging.info(msg)

def pull_latest_github():
    if not Path(LOCAL_PATH, ".git").exists():
        log("📥 Cloning GitHub repo fresh...")
        subprocess.run(["git", "clone", GITHUB_REPO, LOCAL_PATH])
    else:
        log("🔄 Pulling latest from GitHub...")
        subprocess.run(["git", "-C", LOCAL_PATH, "pull"])

def restore_from_mongo():
    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DB][MONGO_COLLECTION]
    log("🔍 Fetching chunked files from MongoDB...")

    sha_index = {}
    for doc in collection.find().sort("timestamp", 1):
        sha = doc["sha"]
        index = doc["index"]
        total_parts = doc["total_parts"]
        data = doc["data"]

        if sha not in sha_index:
            sha_index[sha] = [None] * total_parts
        sha_index[sha][index] = data

    for sha, parts in sha_index.items():
        if None in parts:
            log(f"⚠️ Incomplete file {sha}, skipping.")
            continue

        full_data = b''.join(parts)
        output_path = Path(LOCAL_PATH) / f"rebuild_{sha}.bin"
        with open(output_path, "wb") as f:
            f.write(full_data)
        log(f"✅ Reassembled file: {output_path.name} ({len(full_data)//1024} KB)")

def sync_from_gcs_overlay():
    overlay_path = Path.home() / "Soap_overlay"
    if overlay_path.exists():
        log("☁️ Syncing from GCS overlay...")
        subprocess.run(["cp", "-r", f"{overlay_path}/.", LOCAL_PATH])
    else:
        log("⚠️ GCS overlay not mounted. Skipping GCS restore.")

def rotor_timing_loop():
    while True:
        log("🧠 [Cycle Start] Restoring from all sources...")

        # Phase 1: GitHub pull
        pull_latest_github()
        time.sleep(1.33)

        # Phase 2: Mongo restore
        restore_from_mongo()
        time.sleep(1.33)

        # Phase 3: GCS sync
        sync_from_gcs_overlay()
        time.sleep(1.33)

        log("🔁 [Cycle Complete] Waiting before next rotation...")
        time.sleep(4)

if __name__ == "__main__":
    try:
        log("🚀 Starting Fusion Restore Rotor in background loop...")
        rotor_timing_loop()
    except Exception as e:
        log(f"❌ Exception in rotor: {e}")
