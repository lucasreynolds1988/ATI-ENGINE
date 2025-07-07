#!/usr/bin/env python3
import os
import subprocess

def restore_secrets():
    os.system("python3 ~/Soap/core/fetch_secrets_from_mongo.py")

def git_pull():
    subprocess.run(["git", "pull", "origin", "main"], check=True)

def gcs_restore():
    backup_dir = os.path.expanduser("~/Soap/overlay")
    os.makedirs(backup_dir, exist_ok=True)
    subprocess.run([
        "gsutil", "cp", "gs://ati-oracle-engine/backups/*.zip", backup_dir
    ], check=True)
    print("Backups pulled from GCS.")

if __name__ == "__main__":
    print("Restoring secrets from MongoDB...")
    restore_secrets()
    print("Pulling latest code from GitHub...")
    git_pull()
    print("Restoring from GCS backups...")
    gcs_restore()
    print("All restores complete.")
