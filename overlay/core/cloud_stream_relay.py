import os
import subprocess
from core.rotor_overlay import log_event

# Credentials for GCS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/lucasreynolds1988/Soap/secrets/gcs-creds.json"
GCS_BUCKET = "gs://ati-oracle-engine/backups/"

def stream_to_cloud(file_path):
    try:
        subprocess.run(["gsutil", "cp", file_path, GCS_BUCKET], check=True)
        log_event(f"Streamed {file_path} to GCS bucket.")
    except Exception as e:
        log_event(f"Failed to stream {file_path} to cloud: {e}")

def execute_relay_cycle():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            stream_to_cloud(fpath)
