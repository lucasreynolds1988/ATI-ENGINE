# ~/Soap/core/cloud_stream_relay.py

import os
import subprocess
import json
from core.rotor_overlay import log_event

BASE = os.path.expanduser("~/Soap")
PROTECTED_DIRS = ["core", "agents", "overlay", "eyes", "rotors", "wraps", "triggers"]
MANIFEST_PATH = os.path.join(BASE, "overlay/manifest.json")

def load_manifest_paths():
    if not os.path.exists(MANIFEST_PATH):
        return []
    with open(MANIFEST_PATH, "r") as f:
        return [os.path.expanduser(entry["path"]) for entry in json.load(f)]

def stream_to_cloud(file_path):
    try:
        cmd = [
            "gcloud", "storage", "cp", file_path,
            "gs://ati-cold-storage/", "--parallel-thread-count=4"
        ]
        subprocess.run(cmd, check=True)
        log_event(f"[RELAY] ✅ Uploaded to GCS: {file_path}")

        # Remove only if not protected
        protected = load_manifest_paths()
        if not any(p in file_path for p in PROTECTED_DIRS) and file_path not in protected:
            os.remove(file_path)
            log_event(f"[RELAY] 🧼 Deleted local copy: {file_path}")

    except Exception as e:
        log_event(f"[RELAY] ❌ Upload failed: {str(e)}")

def execute_relay_cycle(file_path):
    stream_to_cloud(file_path)
