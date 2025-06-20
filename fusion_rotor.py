# ~/Soap/fusion_rotor.py

import os
import subprocess
import zipfile
from datetime import datetime
import shutil

def restore_from_github():
    print("🔁 Restoring from GitHub...")
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        print("✅ GitHub restore complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub restore failed: {e}")

def restore_from_gcs():
    print("🔁 Restoring from GCS...")
    try:
        latest = subprocess.check_output([
            "gsutil", "ls", "-l", "gs://ati-rotor-storage/backups/"
        ]).decode()

        latest_zip = sorted([
            line.split()[-1]
            for line in latest.strip().split('\n')
            if line.endswith(".zip")
        ])[-1]

        print(f"📦 Pulling {latest_zip}")
        subprocess.run(["gsutil", "cp", latest_zip, "/tmp/restore.zip"], check=True)

        with zipfile.ZipFile("/tmp/restore.zip", "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove("/tmp/restore.zip")
        print("✅ GCS restore complete.")
    except Exception as e:
        print(f"⚠️ GCS restore failed: {e}")

def restore_from_mongo_stub():
    print("🔁 Restoring from MongoDB stub...")
    try:
        if os.path.exists("rebuild/mongo_stub/"):
            subprocess.run(["cp", "-r", "rebuild/mongo_stub/*", "."], shell=True)
            print("✅ MongoDB restore complete.")
        else:
            print("⚠️ MongoDB stub directory not found, skipping.")
    except Exception as e:
        print(f"❌ MongoDB restore failed: {e}")

def zip_project(source_dir, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(('.pyc', '.log')) or '__pycache__' in root:
                    continue
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, source_dir)
                try:
                    zipf.write(filepath, arcname)
                except Exception as e:
                    print(f"⚠️ Skipped {filepath}: {e}")

def push_to_github():
    print("🔄 Pushing to GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "🌀 Rotor Savepoint: Full system snapshot"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ GitHub push complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub push failed: {e}")

def save_to_gcs(zip_path):
    print("☁️ Uploading to GCS...")
    try:
        subprocess.run(["gsutil", "cp", zip_path, f"gs://ati-rotor-storage/backups/{os.path.basename(zip_path)}"], check=True)
        print("✅ GCS upload complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ GCS upload failed: {e}")

def run_rotor():
    print("🚁 ROTOR FUSION V5 INITIATED — CODE-RED TRIGGERED")

    # STEP 1: Restore from cloud before doing anything else
    restore_from_github()
    restore_from_gcs()
    restore_from_mongo_stub()

    # STEP 2: Now that we’re safe — create new savepoint
    snapshot = f"/tmp/ati_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_project(".", snapshot)
    print(f"📦 Zipped snapshot: {snapshot}")

    # STEP 3: Push to GitHub and GCS
    push_to_github()
    save_to_gcs(snapshot)

    # STEP 4: Cleanup
    os.remove(snapshot)
    print("✅ ROTOR COMPLETE — System synced and protected.")

if __name__ == "__main__":
    run_rotor()
