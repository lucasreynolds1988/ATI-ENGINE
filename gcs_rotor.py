# ~/Soap/gcs_rotor.py

import os
import subprocess
import hashlib
import json
from pathlib import Path

GCS_BUCKET = "gs://ati-rotor-bucket/fusion-backup"
LOG_PATH = os.path.expanduser("~/Soap/.fusion-log.json")

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_log():
    return json.load(open(LOG_PATH)) if os.path.exists(LOG_PATH) else {}

def save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def gcs_upload(file_path):
    try:
        subprocess.run(["gsutil", "cp", str(file_path), GCS_BUCKET], check=True)
        print(f"✅ GCS upload complete: {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ GCS upload failed: {file_path}\n{e}")
        return False

def scan_and_upload():
    log = load_log()
    search_dirs = ["/home", "/root"]

    for base_dir in search_dirs:
        for dirpath, _, filenames in os.walk(base_dir):
            for file in filenames:
                full_path = Path(os.path.join(dirpath, file))
                try:
                    if not full_path.is_file(): continue
                    if full_path.name.startswith("."): continue

                    file_hash = sha256(full_path)
                    if file_hash in log: continue

                    success = gcs_upload(full_path)
                    if success:
                        os.remove(full_path)
                        log[file_hash] = {
                            "path": str(full_path),
                            "dest": "gcs"
                        }
                        print(f"🧹 Deleted: {full_path}")
                except Exception as e:
                    print(f"⚠️ Error on {full_path}: {e}")

    save_log(log)

if __name__ == "__main__":
    scan_and_upload()
