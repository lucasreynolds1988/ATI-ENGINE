import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import hashlib
from core.rotor_overlay import log_event
from core.cloud_stream_relay import stream_to_cloud
from core.mongo_safe_upload_v2 import mongo_safe_upload
from core.fusion_restore_v2 import verify_gcs_file_integrity

ROTATE_DIR = os.path.expanduser("~/Soap/overlay")
DELETION_AFTER_UPLOAD = True  # Set to False to keep local copies

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def run_rotor():
    log_event("Rotor Fusion: Scanning for files...")
    for root, dirs, files in os.walk(ROTATE_DIR):
        for fname in files:
            fpath = os.path.join(root, fname)
            if not os.path.isfile(fpath):
                continue
            sha = sha256sum(fpath)
            log_event(f"Rotor: Processing {fname} | SHA256={sha}")
            try:
                # Route to GCS
                stream_to_cloud(fpath)
                # Route to Mongo if small enough
                if os.path.getsize(fpath) <= 12 * 1024 * 1024:
                    mongo_safe_upload(fpath)
                # Verify integrity (stub)
                verify_gcs_file_integrity(fpath)
                # Delete local copy
                if DELETION_AFTER_UPLOAD:
                    os.remove(fpath)
                    log_event(f"Rotor: Deleted {fpath} after upload")
            except Exception as e:
                log_event(f"Rotor ERROR: {e}")
    log_event("Rotor Fusion: Cycle complete.")

if __name__ == "__main__":
    print("Rotor loop started.")
    while True:
        run_rotor()
        time.sleep(4)
