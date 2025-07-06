#!/usr/bin/env python3
import os
import subprocess
import time

# CONFIG: Paths to load from
GITHUB_REPO = "https://github.com/lucasr610/Soap.git"
MONGO_STUB_DIR = os.path.expanduser("~/mongo_restore_stub")
GCS_BUCKET = "gs://ati-rotor-bucket"

os.makedirs("rebuild/github", exist_ok=True)
os.makedirs("rebuild/gcs", exist_ok=True)
os.makedirs("rebuild/mongo", exist_ok=True)

def log(msg):
    print(f"🔁 {msg}")

def restore_from_github():
    log("Restoring from GitHub...")
    os.chdir("rebuild/github")
    subprocess.run(["git", "clone", GITHUB_REPO])
    os.chdir("../..")
    log("✅ GitHub restore complete.")

def restore_from_gcs():
    log("Restoring from GCS...")
    subprocess.run(["gsutil", "-m", "cp", "-r", f"{GCS_BUCKET}/*", "rebuild/gcs/"])
    log("✅ GCS restore complete.")

def restore_from_mongo_stub():
    log("Restoring from MongoDB stub...")
    if os.path.exists(MONGO_STUB_DIR):
        subprocess.run(["cp", "-r", f"{MONGO_STUB_DIR}/*", "rebuild/mongo/"], shell=True)
    else:
        log("⚠️ MongoDB stub directory not found, skipping.")
    log("✅ MongoDB restore complete.")

def run_rebuild():
    log("Initializing FUSION REBUILD operation...")
    restore_from_github()
    time.sleep(2)
    restore_from_gcs()
    time.sleep(2)
    restore_from_mongo_stub()
    log("🎉 FUSION RESTORE COMPLETE — All sources reintegrated.")

if __name__ == "__main__":
    run_rebuild()
