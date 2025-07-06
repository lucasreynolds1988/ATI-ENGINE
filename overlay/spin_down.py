#!/usr/bin/env python3
import os, json, shutil
from datetime import datetime, timezone
from hashlib import sha256
from core.rotor_overlay import log_event
import subprocess

BACKUP_DIR = os.path.expanduser("~/Soap/backups")
SOURCE_DIR = os.path.expanduser("~/Soap")
MANIFEST_PATH = os.path.expanduser("~/Soap/configs/critical_manifest.json")
GCS_BUCKET = "gs://ati-oracle-engine/backups"

def calculate_sha(file_path):
    sha256_hash = sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def load_manifest():
    with open(MANIFEST_PATH, 'r') as f:
        return json.load(f)['critical_files']

def backup_and_upload():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    temp_backup_dir = os.path.join(SOURCE_DIR, "temp_backup")
    os.makedirs(temp_backup_dir, exist_ok=True)

    # Copy critical files into temp_backup
    manifest = load_manifest()
    for file_info in manifest:
        src_file = os.path.join(SOURCE_DIR, file_info['path'])
        dest_file = os.path.join(temp_backup_dir, file_info['path'])
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dest_file)
        else:
            log_event("SPIN-DOWN", f"Warning: {src_file} not found and skipped.")

    # Create a ZIP archive
    backup_name = f"{BACKUP_DIR}/ATI_FULL_CORE_BACKUP_{timestamp}"
    shutil.make_archive(backup_name, 'zip', temp_backup_dir)
    shutil.rmtree(temp_backup_dir)

    backup_zip = f"{backup_name}.zip"
    sha = calculate_sha(backup_zip)
    log_event("SPIN-DOWN", f"Full core backup created: {backup_zip}, SHA: {sha}")

    # Upload to GCS explicitly
    try:
        subprocess.run(["gsutil", "cp", backup_zip, GCS_BUCKET], check=True)
        log_event("SPIN-DOWN", f"Backup successfully uploaded to {GCS_BUCKET}")
        os.remove(backup_zip)
        log_event("SPIN-DOWN", "Local backup removed after successful upload.")
    except subprocess.CalledProcessError as e:
        log_event("SPIN-DOWN", f"GCS upload failed: {e}")

def main():
    log_event("SPIN-DOWN", "Starting robust full-system spin-down.")
    backup_and_upload()
    log_event("SPIN-DOWN", "Full-system spin-down completed successfully.")

if __name__ == "__main__":
    main()
