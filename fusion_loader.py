# ~/Soap/fusion_loader.py

import os
import subprocess
from pathlib import Path

GITHUB_REPO_URL = "https://github.com/lucasr610/ati-web-app.git"
GITHUB_LOCAL_DIR = os.path.expanduser("~/ati-web-app")

GCS_BUCKET = "gs://ati-sop-backup"
MONGO_STUB_DIR = os.path.expanduser("~/Soap/mongo_stub_restore")

def restore_from_github():
    print("🔁 Restoring from GitHub...")
    if os.path.exists(GITHUB_LOCAL_DIR):
        print("📂 Repo already exists. Pulling latest changes...")
        subprocess.run(["git", "-C", GITHUB_LOCAL_DIR, "pull"], check=True)
    else:
        print("⬇️ Cloning repo fresh...")
        subprocess.run(["git", "clone", GITHUB_REPO_URL, GITHUB_LOCAL_DIR], check=True)
    print("✅ GitHub restore complete.")

def restore_from_gcs():
    print("🔁 Restoring from GCS...")
    try:
        subprocess.run(["gsutil", "-m", "cp", "-r", f"{GCS_BUCKET}/*", str(Path.home())], check=True)
        print("✅ GCS restore complete.")
    except Exception as e:
        print(f"❌ GCS restore failed: {e}")

def restore_from_mongo_stub():
    print("🔁 Restoring from MongoDB stub...")
    if os.path.exists(MONGO_STUB_DIR):
        print("📦 MongoDB stub restore exists — copying into system...")
        for file in os.listdir(MONGO_STUB_DIR):
            src = os.path.join(MONGO_STUB_DIR, file)
            dst = os.path.join(str(Path.home()), file)
            subprocess.run(["cp", "-r", src, dst])
        print("✅ MongoDB restore complete.")
    else:
        print("⚠️ MongoDB stub directory not found, skipping.")

def main():
    print("🔁 Initializing FUSION REBUILD operation...")
    restore_from_github()
    restore_from_gcs()
    restore_from_mongo_stub()
    print("🎉 FUSION RESTORE COMPLETE — All sources reintegrated.")

if __name__ == "__main__":
    main()

