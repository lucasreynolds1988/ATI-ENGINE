#!/usr/bin/env python3
import os
import subprocess

GCS_BUCKET = "gs://ati-oracle-engine/backups/"
TARGET_DIR = os.path.expanduser("~/Soap/restore")
os.makedirs(TARGET_DIR, exist_ok=True)

def gcs_restore():
    print("Listing available GCS backups...")
    subprocess.run(["gsutil", "ls", GCS_BUCKET])
    filename = input("Enter backup filename (e.g., ATI_FULL_CORE_BACKUP_20250704_071731.zip): ")
    full_gcs_path = GCS_BUCKET + filename
    target_zip = os.path.join(TARGET_DIR, filename)
    subprocess.run(["gsutil", "cp", full_gcs_path, target_zip], check=True)
    subprocess.run(["unzip", "-o", target_zip, "-d", TARGET_DIR], check=True)
    print(f"Restored GCS backup to {TARGET_DIR}")

if __name__ == "__main__":
    gcs_restore()
