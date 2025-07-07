#!/usr/bin/env python3
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import subprocess
from core.rotor_overlay import log_event

# Google Cloud credentials and GCS target
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/lucasreynolds1988/Soap/secrets/gcs-creds.json"
GCS_BUCKET = "gs://ati-oracle-engine/backups/"

def stream_to_cloud(file_path):
    try:
        subprocess.run([
            "gsutil",
            "-o", "GSUtil:parallel_composite_upload_threshold=150M",
            "cp", file_path, GCS_BUCKET
        ], check=True)
        log_event(f"[RELAY] 🚀 Parallel upload (composite) to GCS: {file_path}")
    except Exception as e:
        log_event(f"[RELAY] ❌ Upload failed: {file_path} | {e}")

def execute_relay_cycle():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            stream_to_cloud(fpath)

if __name__ == "__main__":
    execute_relay_cycle()
