# ~/Soap/fusion_restore_v2.py

import os
import sys
import json
import base64
import hashlib
import subprocess
from pymongo import MongoClient

# === CONFIGURATION ===
RESTORE_DIR = os.path.expanduser("~/Soap_overlay")
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
DB_NAME = "fusion"
COLLECTION_NAME = "files"
GITHUB_REPO_DIR = "/home/lucasreynolds1988/Soap"
GCS_BUCKET_PATH = "gs://ati-rotor-bucket/fusion-backup/*"

# === UTILS ===
def compute_sha256(data):
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()

# === MONGODB RESTORE ===
def restore_file_by_filename(filename):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        chunks = list(collection.find({"filename": filename}))
        if not chunks:
            print(f"❌ No chunks found for: {filename}")
            return

        chunks.sort(key=lambda x: x["chunk_index"])
        data = b''.join(base64.b64decode(chunk["chunk_data"]) for chunk in chunks)

        save_path = os.path.join(RESTORE_DIR, filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(data)

        sha = compute_sha256(data)
        print(f"✅ Restored: {filename} [{len(chunks)} chunks] [SHA256: {sha}]")

    except Exception as e:
        print(f"❌ Error restoring {filename}: {e}")

def restore_all_unique_files():
    print("🔁 Restoring all files from MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    filenames = collection.distinct("filename")
    for fname in filenames:
        restore_file_by_filename(fname)

# === GCS RESTORE ===
def restore_from_gcs():
    print("\n🔁 Restoring from GCS...")
    try:
        subprocess.run([
            "gsutil", "-m", "cp", "-r",
            GCS_BUCKET_PATH, RESTORE_DIR
        ], check=True)
        print("✅ GCS restore complete.")
    except Exception as e:
        print(f"❌ GCS restore failed: {e}")

# === GITHUB RESTORE ===
def restore_from_git():
    print("\n🔁 Pulling latest from GitHub...")
    try:
        subprocess.run(["git", "-C", GITHUB_REPO_DIR, "pull"], check=True)
        print("✅ GitHub pull complete.")
    except Exception as e:
        print(f"❌ GitHub pull failed: {e}")

# === SPIN-UP TRIGGER ===
def launch_spin_up():
    print("\n🌀 Launching +SPIN-UP+ sequence...")
    try:
        subprocess.run(["python3", "/home/lucasreynolds1988/Soap/spin_up.py"], check=True)
    except Exception as e:
        print(f"❌ +SPIN-UP+ launch failed: {e}")

# === MAIN ENTRY ===
def main():
    os.makedirs(RESTORE_DIR, exist_ok=True)

    if len(sys.argv) == 1:
        restore_all_unique_files()
    elif len(sys.argv) == 2:
        target = sys.argv[1]
        if target.endswith(".json"):
            try:
                with open(target, "r") as f:
                    manifest = json.load(f)
                file_list = manifest.get("files", [])
                if not file_list:
                    print(f"❌ Manifest is empty: {target}")
                    sys.exit(1)
                for fname in file_list:
                    restore_file_by_filename(fname)
            except Exception as e:
                print(f"❌ Failed to process manifest {target}: {e}")
                sys.exit(1)
        else:
            restore_file_by_filename(target)
    else:
        print("Usage: python3 fusion_restore_v2.py [<filename> | <manifest.json>]")
        print("Leave blank to restore everything from MongoDB.")
        sys.exit(1)

    restore_from_gcs()
    restore_from_git()
    launch_spin_up()

    print(f"\n🎉 FUSION RESTORE COMPLETE — All sources reintegrated into: {RESTORE_DIR}")

if __name__ == "__main__":
    main()
