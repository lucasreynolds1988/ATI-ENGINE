#!/usr/bin/env python3
import subprocess
from core.rotor_overlay import log_event

def upload_to_gcs(file_path, bucket):
    try:
        subprocess.run(["gsutil", "cp", file_path, bucket], check=True)
        log_event("GCS_UPLOADER", f"Uploaded successfully: {file_path} → {bucket}")
    except subprocess.CalledProcessError as e:
        log_event("GCS_UPLOADER", f"Upload failed for {file_path}: {e}")
