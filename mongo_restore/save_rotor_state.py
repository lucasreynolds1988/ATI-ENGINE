#!/usr/bin/env python3
import os
import time
import subprocess
from datetime import datetime

# === CONFIG ===
BACKUP_DIR = os.path.expanduser("~/Soap")
ZIP_PREFIX = "system_backup"
GCS_BUCKET = "gs://ati-system-backups"

# === ROTOR FILES TO VERIFY ===
REQUIRED_FILES = [
    "rotor_fusion.py",
    "code_red.py",
    "spin_up.py",
    "cloud_stream_relay.py",
    "warm_start_engine.py",
    "agents/arbiter_phase.py",
    "agents/mother_phase.py",
    "agents/father_phase.py",
    "agents/watson_phase.py",
    "agents/soap_phase.py",
    "core/rotor_overlay.py"
]

def verify_files():
    print("[🔍] Verifying rotor files...")
    for rel_path in REQUIRED_FILES:
        full_path = os.path.join(BACKUP_DIR, rel_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"❌ MISSING: {rel_path}")
    print("[✅] All required rotor files verified.")

def create_zip():
    timestamp = int(time.time())
    zip_name = f"{ZIP_PREFIX}_{timestamp}.zip"
    zip_path = os.path.join(BACKUP_DIR, zip_name)

    print(f"[📦] Creating backup zip: {zip_name}")
    subprocess.run([
        "zip", "-r", zip_name,
        "rotor_fusion.py", "code_red.py", "spin_up.py",
        "cloud_stream_relay.py", "warm_start_engine.py",
        "agents", "core", "memory"
    ], cwd=BACKUP_DIR, check=True)

    return zip_path

def upload_to_gcs(zip_path):
    print(f"[☁️] Uploading to GCS: {GCS_BUCKET}")
    subprocess.run(["gsutil", "cp", zip_path, GCS_BUCKET], check=True)

def rotate_backups():
    print("[♻️] Rotating backups (keeping 2 newest)...")
    result = subprocess.run(
        ["gsutil", "ls", GCS_BUCKET],
        capture_output=True, text=True, check=True
    )
    backups = sorted(
        [line.strip() for line in result.stdout.splitlines() if ZIP_PREFIX in line],
        reverse=True
    )
    if len(backups) > 2:
        old = backups[2:]
        for path in old:
            print(f"[🗑️] Deleting old backup: {path}")
            subprocess.run(["gsutil", "rm", path], check=True)

def cleanup_local_zips():
    print("[🧹] Cleaning up local zip files...")
    for f in os.listdir(BACKUP_DIR):
        if f.startswith(ZIP_PREFIX) and f.endswith(".zip"):
            os.remove(os.path.join(BACKUP_DIR, f))

if __name__ == "__main__":
    try:
        verify_files()
        zip_path = create_zip()
        upload_to_gcs(zip_path)
        rotate_backups()
        cleanup_local_zips()
        print("[✅] Rotor state saved and secured.")
    except Exception as e:
        print(f"[❌ ERROR] {e}")
