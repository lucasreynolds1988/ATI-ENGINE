# ~/Soap/overlay/code_red.py

import os
import hashlib
from core.rotor_overlay import log_event
from core.cleanup_utils import clear_bloat
from core.fusion_manifest import load_manifest_paths
from core.mongo_safe_upload_v2 import upload_file_to_mongo

MAX_PUSH_MB = 80
MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB = "ati_engine"
MONGO_COLLECTION = "code_red_snapshots"

def sha256(file_path):
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

def code_red():
    log_event("🧨 CODE-RED: Emergency upload triggered.")
    clear_bloat()
    manifest_paths = load_manifest_paths()

    for base in manifest_paths:
        base = os.path.expanduser(base)
        if not os.path.exists(base):
            continue

        for root, dirs, files in os.walk(base):
            for file in files:
                file_path = os.path.join(root, file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if size_mb <= MAX_PUSH_MB:
                    log_event(f"📤 Uploading {file_path} to MongoDB...")
                    upload_file_to_mongo(file_path, MONGO_URI, MONGO_DB, MONGO_COLLECTION)
                else:
                    log_event(f"⚠️ Skipped (too large): {file_path}")

    log_event("✅ CODE-RED complete. System safe snapshot uploaded.")

if __name__ == "__main__":
    code_red()

