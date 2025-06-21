# ~/Soap/fusion_rebuild_from_log.py

import json
import gzip
import subprocess
from pathlib import Path
from datetime import datetime
from pymongo import MongoClient
from bson.binary import Binary

# === CONFIG ===
LOG_PATH = Path.home() / "Soap/data/relay_log.json"
STATE_DIR = Path.home() / "Soap/fusion_rebuild"
GCS_BUCKET = "gs://ati-rotor-fusion/stream"
GITHUB_DIR = Path.home() / "Soap/github_stream_staging"
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
DB = MongoClient(MONGO_URI).fusion

# === PREP ===
STATE_DIR.mkdir(parents=True, exist_ok=True)

def load_log():
    if not LOG_PATH.exists():
        print("❌ Log not found.")
        return []
    with open(LOG_PATH, "r") as f:
        return json.load(f)

def choose_entry(log):
    print(f"\n🧬 Total: {len(log)} log entries")
    for idx, entry in enumerate(log):
        ts = datetime.fromisoformat(entry["timestamp"])
        print(f"{idx:>3} | {entry['target']:<8} | {ts.strftime('%Y-%m-%d %H:%M:%S')} | {entry['chunk_id']}")
    try:
        i = int(input("\nSelect index to rebuild: "))
        return log[i]
    except:
        print("⚠️ Invalid selection.")
        return None

def from_mongo(chunk_id):
    doc = DB.file_chunks.find_one({"chunk_id": chunk_id})
    if not doc:
        print("❌ Not found in Mongo.")
        return None
    return doc["data"]

def from_gcs(chunk_id):
    remote = f"{GCS_BUCKET}/{chunk_id}.gz"
    local = STATE_DIR / f"{chunk_id}.gz"
    try:
        subprocess.run(["gsutil", "cp", remote, str(local)], check=True)
        return local.read_bytes()
    except Exception as e:
        print(f"❌ GCS error: {e}")
        return None

def from_github(chunk_id):
    path = GITHUB_DIR / f"{chunk_id}.gz"
    if not path.exists():
        print("❌ Not found in GitHub staging.")
        return None
    return path.read_bytes()

def decompress_and_run(chunk_id, data_gz):
    try:
        raw = gzip.decompress(data_gz).decode()
        print(f"\n🔓 Recovered chunk {chunk_id}:\n" + "="*40)
        print(raw)
        print("="*40)
        if "#RUNTIME" in raw:
            exec(input("⚙️ Execute this stream? (y/N): ").strip().lower() == "y" and raw or "", globals())
    except Exception as e:
        print(f"❌ Decompress error: {e}")

def main():
    log = load_log()
    if not log:
        return

    entry = choose_entry(log)
    if not entry:
        return

    cid = entry["chunk_id"]
    source = entry["target"]

    print(f"\n🔁 Rebuilding from: {source} [{cid}]")

    if source == "MongoDB":
        data = from_mongo(cid)
    elif source == "GCS":
        data = from_gcs(cid)
    elif source == "GitHub":
        data = from_github(cid)
    else:
        print("❌ Unknown source.")
        return

    if data:
        decompress_and_run(cid, data)

if __name__ == "__main__":
    main()
