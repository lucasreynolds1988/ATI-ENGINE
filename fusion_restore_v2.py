#!/usr/bin/env python3
import os, subprocess, logging, sys, time
from pathlib import Path
from pymongo import MongoClient
from google.cloud import storage

HOME_DIR = Path.home()
SOAP_DIR = HOME_DIR / "Soap"
LOG_DIR = SOAP_DIR / "data/logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s", handlers=[
    logging.FileHandler(LOG_DIR / "fusion_restore.log"),
    logging.StreamHandler(sys.stdout)
])

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Service2244%23%23@ai-sop-dev.nezgetk.mongodb.net")
GCS_BUCKET = "ati-oracle-engine"
GCS_OVERLAY_PATH = "overlay/"

def pull_latest_github():
    logging.info("🔄 Pulling latest from GitHub explicitly...")
    subprocess.run(["git", "-C", str(SOAP_DIR), "pull"], check=False)

def restore_from_mongo():
    logging.info("📦 Explicitly restoring files from MongoDB...")
    client = MongoClient(MONGO_URI)
    coll = client["rotor"]["fusion_chunks"]
    docs = coll.aggregate([{"$sort": {"timestamp": 1}}])
    for doc in docs:
        sha, idx, total, data = doc["sha"], doc["index"], doc["total_parts"], doc["data"]
        file = SOAP_DIR / f"rebuild_{sha}.bin"
        file.write_bytes(data)
        logging.info(f"✅ Explicitly restored {file.name} from MongoDB.")

def restore_from_gcs():
    logging.info("☁️ Explicitly syncing overlay from GCS...")
    client = storage.Client()
    blobs = client.list_blobs(GCS_BUCKET, prefix=GCS_OVERLAY_PATH)
    for blob in blobs:
        rel_path = Path(blob.name).relative_to(GCS_OVERLAY_PATH)
        # Explicitly prevent overwriting secrets
        if str(rel_path).startswith("secrets/"):
            logging.info(f"🔒 Skipping protected file {rel_path}")
            continue
        dest_file = SOAP_DIR / rel_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(dest_file)
        logging.info(f"⬇️ Explicitly downloaded {rel_path}")
    logging.info("✅ GCS overlay explicitly synced successfully.")

def rotor_loop():
    while True:
        logging.info("🔄 Starting explicit restore cycle.")
        pull_latest_github()
        restore_from_mongo()
        restore_from_gcs()
        logging.info("✅ Explicit restore cycle complete. Waiting 4s...")
        time.sleep(4)

if __name__ == "__main__":
    rotor_loop()
