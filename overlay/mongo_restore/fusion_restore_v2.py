#!/usr/bin/env python3
import asyncio
import subprocess
import os
import shutil
import time

HOME_DIR = os.path.expanduser("~")
SOAP_DIR = os.path.join(HOME_DIR, "Soap")
BACKUP_DIR = os.path.join(SOAP_DIR, "cloud_backup")

# Local save state (your original logic)
def save_state():
    print("🧭 Saving system state to backup...")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for item in os.listdir(SOAP_DIR):
        s = os.path.join(SOAP_DIR, item)
        d = os.path.join(BACKUP_DIR, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print("✅ System state saved to cloud_backup.")

# Local restore state (your original logic)
def restore_state():
    print("🧭 Restoring system state from backup...")
    if not os.path.exists(BACKUP_DIR):
        print("❌ No backup found!")
        return
    for item in os.listdir(BACKUP_DIR):
        s = os.path.join(BACKUP_DIR, item)
        d = os.path.join(SOAP_DIR, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print("✅ System restore complete.")

# GitHub pull: lightweight
async def github_pull():
    proc = await asyncio.create_subprocess_shell(
        "git pull origin main",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        print("[INFO] ✅ GitHub synced successfully.")
    else:
        print(f"[ERROR] ❌ GitHub sync failed: {stderr.decode()}")

# MongoDB restore: restoring binary files
async def mongo_restore():
    await asyncio.to_thread(mongo_restore_function)

def mongo_restore_function():
    from mongo_safe_upload_v2 import MongoChunker
    chunker = MongoChunker()
    restored_files = chunker.restore_files()
    for file in restored_files:
        print(f"[INFO] ✅ Restored {file} from MongoDB.")

# GCS syncing overlay files
async def gcs_sync():
    await asyncio.to_thread(gcs_sync_function)

def gcs_sync_function():
    from google.cloud import storage

    client = storage.Client.from_service_account_json('secrets/gcs-creds.json')
    bucket = client.get_bucket("ati-oracle-engine")
    overlay_prefix = "overlay/"
    blobs = bucket.list_blobs(prefix=overlay_prefix)

    for blob in blobs:
        local_path = os.path.join(SOAP_DIR, blob.name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        if blob.name.endswith(('gcs-creds.json', 'github-token.txt', 'mongo-creds.json')):
            print(f"[INFO] 🔒 Skipping protected file {blob.name}")
            continue

        blob.download_to_filename(local_path)
        print(f"[INFO] ⬇️ Explicitly downloaded {blob.name}")

# Unified explicit restore cycle (async zero-state model)
async def explicit_restore_cycle():
    interval = 4  # 4-second intervals
    while True:
        start_time = time.time()

        print("[INFO] 🔄 Starting explicit restore cycle.")
        await asyncio.gather(
            github_pull(),
            mongo_restore(),
            gcs_sync()
        )

        elapsed = time.time() - start_time
        sleep_duration = max(0, interval - elapsed)
        print(f"[INFO] ⏳ Cycle complete in {elapsed:.2f}s, sleeping for {sleep_duration:.2f}s.")
        await asyncio.sleep(sleep_duration)

# Main function to handle CLI arguments and run loop
def main():
    import sys
    if "--save" in sys.argv:
        save_state()
    elif "--restore-local" in sys.argv:
        restore_state()
    else:
        asyncio.run(explicit_restore_cycle())

if __name__ == "__main__":
    main()
