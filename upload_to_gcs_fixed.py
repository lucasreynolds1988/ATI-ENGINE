# ~/Soap/upload_to_gcs_fixed.py

import sys
import os
from google.cloud import storage

BUCKET_NAME = "ati-rotor-bucket"

def upload_file_to_gcs(file_path):
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    print(f"🚀 Uploading {file_path} to GCS bucket '{BUCKET_NAME}'...")

    try:
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        print(f"✅ Upload complete: {blob.public_url}")
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 upload_to_gcs_fixed.py <file_path>")
    else:
        upload_file_to_gcs(sys.argv[1])
