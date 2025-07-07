#!/usr/bin/env python3
import subprocess
from core.rotor_overlay import log_event

def stream_to_cloud(file_path):
    try:
        log_event("CLOUD_STREAM_RELAY", f"Starting cloud stream relay for {file_path}")
        # Replace the bucket name with your actual bucket name
        bucket = "gs://ati-oracle-engine/backups/"
        subprocess.run(["gsutil", "cp", file_path, bucket], check=True)
        log_event("CLOUD_STREAM_RELAY", f"Successfully streamed {file_path} to cloud storage.")
    except subprocess.CalledProcessError as e:
        log_event("CLOUD_STREAM_RELAY", f"Failed to stream {file_path}: {e}")
