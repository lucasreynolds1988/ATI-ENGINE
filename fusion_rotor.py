# ~/Soap/fusion_rotor.py

import os
import subprocess
from pymongo import MongoClient
import gridfs
from google.cloud import storage

# === MongoDB Upload ===
def push_to_mongodb(file_path):
    try:
        print(f"[MONGODB] ⬆️ Uploading {file_path}...")

        client = MongoClient("mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
        db = client["rotor_storage"]
        fs = gridfs.GridFS(db)

        file_name = os.path.basename(file_path)
        existing = db.fs.files.find_one({"filename": file_name})
        if existing:
            fs.delete(existing["_id"])

        with open(file_path, "rb") as f:
            fs.put(f, filename=file_name)

        print(f"[MONGODB] ✅ {file_name} uploaded to MongoDB.")
    except Exception as e:
        print(f"[MONGODB] ❌ {file_path} failed: {e}")

# === GitHub Upload ===
def push_to_github(file_path):
    try:
        print(f"[GITHUB] ⬆️ Committing {file_path} to GitHub...")

        repo_path = os.path.expanduser("~/Soap")  # adjust if needed
        rel_path = os.path.relpath(file_path, repo_path)

        subprocess.run(["git", "-C", repo_path, "add", rel_path], check=True)
        subprocess.run(["git", "-C", repo_path, "commit", "-m", f"🔄 Auto-commit: {rel_path}"], check=True)
        subprocess.run(["git", "-C", repo_path, "push"], check=True)

        print(f"[GITHUB] ✅ {rel_path} pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"[GITHUB] ❌ Failed to push {file_path}: {e}")

# === Google Cloud Storage Upload ===
def push_to_gcs(file_path):
    try:
        print(f"[GCS] ⬆️ Uploading {file_path} to Google Cloud Storage...")

        bucket_name = "vivid-fragment-462823-r7.appspot.com"  # change to your GCS bucket
        destination_blob_name = os.path.basename(file_path)

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(file_path)

        print(f"[GCS] ✅ Uploaded {destination_blob_name} to {bucket_name}")
    except Exception as e:
        print(f"[GCS] ❌ Failed to upload {file_path}: {e}")
