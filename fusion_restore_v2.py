#!/usr/bin/env python3
"""
fusion_restore_v2.py: Restore local files from GitHub, MongoDB, and GCS overlay
in a timed rotor loop.
Usage:
  python3 fusion_restore_v2.py
"""
import os
import time
import subprocess
import logging
import sys
from pathlib import Path
from pymongo import MongoClient

HOME_DIR = Path.home()
SOAP_DIR = HOME_DIR / "Soap"
LOG_DIR = SOAP_DIR / "data" / "logs"
LOG_FILE = LOG_DIR / "restore.log"
GITHUB_REPO = "https://github.com/lucasr610/Soap.git"
GCS_OVERLAY_DIR = HOME_DIR / "Soap_overlay"
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net")
MONGO_DB = "rotor"
MONGO_COLL = "fusion_chunks"
CYCLE_INTERVAL = 4  # seconds between cycles

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(console)

logger = logging.getLogger()

def log(msg, level=logging.INFO):
    logger.log(level, msg)

def pull_latest_github():
    if not (SOAP_DIR / ".git").exists():
        log("📥 Cloning GitHub repo...", logging.INFO)
        subprocess.run(["git", "clone", GITHUB_REPO, str(SOAP_DIR)], check=False)
    else:
        log("🔄 Pulling latest from GitHub...", logging.INFO)
        subprocess.run(["git", "-C", str(SOAP_DIR), "pull"], check=False)

def restore_from_mongo():
    log("🔍 Restoring chunked files from MongoDB...", logging.INFO)
    try:
        client = MongoClient(MONGO_URI)
        coll = client[MONGO_DB][MONGO_COLL]
        cursor = coll.aggregate([{"$sort": {"timestamp": 1}}], allowDiskUse=True)
    except Exception as e:
        log(f"❌ MongoDB error: {e}", logging.ERROR)
        return

    file_chunks = {}
    for doc in cursor:
        sha = doc.get("sha")
        idx = doc.get("index")
        total = doc.get("total_parts")
        data = doc.get("data")
        file_chunks.setdefault(sha, {"total": total, "chunks": {}})["chunks"][idx] = data

    for sha, info in file_chunks.items():
        if len(info["chunks"]) != info["total"]:
            log(f"⚠️ Incomplete chunks for {sha}, skipping.", logging.WARNING)
            continue
        try:
            assembled = b"".join(info["chunks"][i] for i in range(info["total"]))
            out_file = SOAP_DIR / f"rebuild_{sha}.bin"
            out_file.write_bytes(assembled)
            log(f"✅ Reassembled {out_file.name}", logging.INFO)
        except Exception as e:
            log(f"❌ Failed writing {out_file.name}: {e}", logging.ERROR)

def sync_gcs_overlay():
    if GCS_OVERLAY_DIR.exists():
        log("☁️ Syncing from GCS overlay...", logging.INFO)
        subprocess.run(["cp", "-r", f"{GCS_OVERLAY_DIR}/.", str(SOAP_DIR)], check=False)
    else:
        log("⚠️ GCS overlay not found, skipping.", logging.WARNING)

def rotor_timing_loop():
    while True:
        log("🧠 [Cycle Start] Executing restore cycle...", logging.INFO)
        pull_latest_github()
        time.sleep(1)
        restore_from_mongo()
        time.sleep(1)
        sync_gcs_overlay()
        log("🔁 [Cycle Complete] Waiting before next cycle...", logging.INFO)
        time.sleep(CYCLE_INTERVAL)

def main():
    setup_logging()
    log("🚀 Starting fusion_restore_v2 rotor...", logging.INFO)
    try:
        rotor_timing_loop()
    except KeyboardInterrupt:
        log("🛑 Stopping restore rotor (KeyboardInterrupt)", logging.INFO)
    except Exception as e:
        log(f"❌ Unexpected error: {e}", logging.ERROR)
        sys.exit(1)

if __name__ == "__main__":
    main()
