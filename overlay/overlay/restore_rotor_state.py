#!/usr/bin/env python3
import subprocess
import os
import argparse

BUCKET = "gs://ati-system-backups"
DEST_DIR = os.path.expanduser("~/Soap")
ZIP_PREFIX = "system_backup"

def get_backup_list():
    result = subprocess.run(["gsutil", "ls", BUCKET], capture_output=True, text=True, check=True)
    backups = sorted(
        [line.strip() for line in result.stdout.splitlines() if ZIP_PREFIX in line],
        reverse=True
    )
    if len(backups) < 2:
        raise Exception("Not enough backups found in GCS.")
    return backups

def download_and_extract(backup_url):
    zip_filename = os.path.basename(backup_url)
    local_path = os.path.join(DEST_DIR, zip_filename)

    print(f"[☁️] Downloading: {zip_filename}")
    subprocess.run(["gsutil", "cp", backup_url, local_path], check=True)

    print(f"[📂] Extracting into {DEST_DIR}")
    subprocess.run(["unzip", "-o", local_path, "-d", DEST_DIR], check=True)

    print(f"[🧹] Removing zip file: {zip_filename}")
    os.remove(local_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--older", action="store_true", help="Restore the older of the two latest backups")
    args = parser.parse_args()

    try:
        backups = get_backup_list()
        chosen_backup = backups[1] if args.older else backups[0]

        print(f"[🔄] Restoring from: {chosen_backup}")
        download_and_extract(chosen_backup)

        print("[✅] Restore complete.")
    except Exception as e:
        print(f"[❌ ERROR] {e}")
