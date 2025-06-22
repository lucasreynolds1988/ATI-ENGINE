# ~/Soap/stream_memory.py

import time
import os
import hashlib
import subprocess
from pathlib import Path

GCS_BUCKET = "gs://ati-rotor-bucket/stream-memory"
TEMP_PATH = Path("/tmp/memory_stream.txt")
CHUNK_SIZE = 512 * 1024  # 512KB

def generate_dummy_data(size_mb=10):
    print(f"🔧 Generating {size_mb}MB of dummy data...")
    try:
        with open(TEMP_PATH, "wb") as f:
            f.write(os.urandom(size_mb * 1024 * 1024))
    except Exception as e:
        print(f"❌ Failed to generate data: {e}")

def compute_sha(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        print(f"❌ SHA computation error: {e}")
        return "ERROR_SHA"

def upload_to_gcs(path):
    print(f"☁️ Uploading to GCS: {path.name}")
    try:
        subprocess.run(["gsutil", "cp", str(path), GCS_BUCKET], check=True)
        print("✅ Upload complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ GCS upload failed: {e}")

def stream_simulation_loop():
    print("🔁 Starting stream memory simulation (GCS as RAM)...")
    while True:
        if not TEMP_PATH.exists():
            generate_dummy_data()

        sha = compute_sha(TEMP_PATH)
        print(f"📡 Memory stream SHA: {sha[:12]}")

        upload_to_gcs(TEMP_PATH)

        try:
            TEMP_PATH.unlink()
            print("🧹 Temp file cleared.")
        except Exception as e:
            print(f"⚠️ Failed to delete temp file: {e}")

        time.sleep(4)

if __name__ == "__main__":
    stream_simulation_loop()
