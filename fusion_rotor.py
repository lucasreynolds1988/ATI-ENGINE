# ~/Soap/fusion_rotor.py

import os
import shutil
import subprocess
from datetime import datetime
import zipfile

def zip_project(source_dir, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(('.pyc', '.log')) or '__pycache__' in root:
                    continue
                try:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, source_dir)
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
    bucket = "ati-rotor-storage"
    dest = f"backups/{os.path.basename(zip_path)}"
    print(f"☁️ Uploading {zip_path} to GCS bucket {bucket}...")
    try:
        subprocess.run(["gsutil", "cp", zip_path, f"gs://{bucket}/{dest}"], check=True)
        print("✅ GCS upload complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ GCS upload failed: {e}")

def run_rotor():
    print("🚁 ROTOR FUSION STARTED — Preparing snapshot...")
    snapshot_name = f"ati_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = f"/tmp/{snapshot_name}"
    zip_project(".", zip_path)
    print(f"📦 Project zipped: {zip_path}")

    push_to_github()
    save_to_gcs(zip_path)

    print("🧹 Cleaning up temp archive...")
    try:
        os.remove(zip_path)
    except:
        pass
    print("✅ ROTOR COMPLETE — System fully backed up.")

if __name__ == "__main__":
    run_rotor()
