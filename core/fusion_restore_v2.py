# ~/Soap/core/fusion_restore_v2.py

import os
import json
from core.rotor_overlay import log_event
from core.mongo_safe_upload_v2 import fetch_chunks_from_mongo

RESTORE_DIR = os.path.expanduser("~/Soap/")

def restore_from_manifest(manifest):
    for file_entry in manifest.get("files", []):
        path = os.path.join(RESTORE_DIR, file_entry["path"].replace("~/Soap/", ""))
        source = file_entry.get("source", "unknown")
        sha = file_entry.get("sha256", "")
        
        if source == "mongo":
            log_event(f"🔁 Restoring from MongoDB: {file_entry['path']}")
            fetch_chunks_from_mongo(file_entry['path'], sha, RESTORE_DIR)

        elif source == "gcs":
            log_event(f"☁️ GCS restore not yet implemented for: {file_entry['path']}")

        elif source == "github":
            log_event(f"🔃 GitHub pull not supported in restore_from_manifest yet.")

        else:
            log_event(f"❓ Unknown source for {file_entry['path']}, skipping.")
