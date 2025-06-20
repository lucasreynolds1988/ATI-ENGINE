import os
import json
import subprocess
from pathlib import Path

GITHUB_RAW_PREFIX = "https://raw.githubusercontent.com/lucasr610/Soap/main"
GCS_BUCKET = "gs://ati-rotor-bucket/fusion-backup"
FUSION_LOG = os.path.expanduser("~/Soap/.fusion-log.json")
RESTORE_DIR = os.path.expanduser("~/Soap/fusion_restored")

def load_log():
    if os.path.exists(FUSION_LOG):
        with open(FUSION_LOG, "r") as f:
            return json.load(f)
    return {}

def rebuild_from_github(file_record):
    rel_path = os.path.relpath(file_record["path"], "/home/lucasreynolds1988/Soap")
    url = f"{GITHUB_RAW_PREFIX}/{rel_path}"
    target_path = os.path.join(RESTORE_DIR, os.path.basename(file_record["path"]))
    print(f"🌐 GitHub → {target_path}")
    subprocess.run(["curl", "-sSL", url, "-o", target_path])
    print(f"✅ Restored from GitHub")

def rebuild_from_gcs(file_record):
    target_path = os.path.join(RESTORE_DIR, os.path.basename(file_record["path"]))
    print(f"☁️ GCS → {target_path}")
    subprocess.run(["gsutil", "cp", f"{GCS_BUCKET}/{os.path.basename(file_record['path'])}", target_path])
    print(f"✅ Restored from GCS")

def rebuild_from_mongo(file_record):
    print(f"🧬 MongoDB restore STUB — {file_record['path']}")

def restore_all():
    os.makedirs(RESTORE_DIR, exist_ok=True)
    log = load_log()
    if not log:
        print("❌ No entries found in fusion log.")
        return
    for file_hash, record in log.items():
        dest = record["dest"]
        print(f"🔁 Restoring: {record['path']} ({dest})")
        if dest == "github":
            rebuild_from_github(record)
        elif dest == "gcs":
            rebuild_from_gcs(record)
        elif dest == "mongo":
            rebuild_from_mongo(record)
    print("✅ All recoverable files processed.")

if __name__ == "__main__":
    print("🧬 Fusion Rebuilder auto-mode initiated")
    restore_all()
