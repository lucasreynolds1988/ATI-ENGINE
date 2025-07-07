# ~/Soap/rotor_gcs.py

import os
import time
from datetime import datetime
from pathlib import Path
from google.cloud import storage

UPLOAD_PATH = Path.home() / "Soap/upload"
LOG_PATH = Path.home() / "Soap/logs/rotor_gcs.log"
BUCKET_NAME = "ati-rotor-coldstore"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(Path.home() / ".gcp_credentials.json")
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

def upload_to_gcs():
    for file in UPLOAD_PATH.iterdir():
        if file.is_file():
            blob = bucket.blob(file.name)
            try:
                blob.upload_from_filename(str(file))
                log(f"✅ Uploaded to GCS: {file.name}")
                file.unlink()
            except Exception as e:
                log(f"❌ GCS Upload Error: {file.name} - {e}")

def main():
    while True:
        upload_to_gcs()
        time.sleep(6)

if __name__ == "__main__":
    main()
