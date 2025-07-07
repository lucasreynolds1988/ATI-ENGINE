#!/usr/bin/env python3
import os
import subprocess
import datetime
import sys

def git_push():
    print("[GitHub] Adding and committing changes...")
    subprocess.run(["git", "add", "."], check=True)
    try:
        subprocess.run(["git", "commit", "-m", "Automated save: code, logic, assets"], check=True)
    except subprocess.CalledProcessError:
        print("[GitHub] No new changes to commit.")
    print("[GitHub] Pushing to remote...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("[GitHub] ✅ Done.")

def gcs_backup():
    print("[GCS] Zipping project and uploading backup...")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"ATI_BACKUP_{ts}.zip"
    soap_dir = os.path.expanduser("~/Soap")
    subprocess.run(["zip", "-r", backup_name, "./"], cwd=soap_dir, check=True)
    # Make sure you have gsutil installed and configured!
    subprocess.run(["gsutil", "cp", backup_name, "gs://ati-oracle-engine/backups/"], cwd=soap_dir, check=True)
    print(f"[GCS] ✅ Uploaded backup {backup_name} to GCS.")
    # Optionally delete zip to save space
    os.remove(os.path.join(soap_dir, backup_name))
    print(f"[GCS] Deleted local zip {backup_name} to save space.")

def mongo_secrets():
    print("[MongoDB] Uploading secrets to MongoDB...")
    subprocess.run(["python3", os.path.expanduser("~/Soap/core/upload_secrets_to_mongo.py")], check=True)
    print("[MongoDB] ✅ All secrets uploaded.")

if __name__ == "__main__":
    try:
        git_push()
    except Exception as e:
        print(f"[GitHub] ERROR: {e}", file=sys.stderr)
    try:
        gcs_backup()
    except Exception as e:
        print(f"[GCS] ERROR: {e}", file=sys.stderr)
    try:
        mongo_secrets()
    except Exception as e:
        print(f"[MongoDB] ERROR: {e}", file=sys.stderr)
    print("=== Universal Save Complete! ===")
