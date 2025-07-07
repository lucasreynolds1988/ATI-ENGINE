import os
import time
import hashlib
from core.rotor_overlay import log_event
from core.cloud_stream_relay import stream_to_cloud, execute_relay_cycle
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
            # Route to cloud (GCS)
            stream_to_cloud(fpath)
            # Route to MongoDB if small enough
            if os.path.getsize(fpath) <= 12*1024*1024:
                mongo_safe_upload(fpath)
            # Optionally verify upload
            verify_gcs_file_integrity(fpath)
            # Delete local after upload
            if DELETION_AFTER_UPLOAD:
                os.remove(fpath)
                log_event(f"Deleted {fpath} after upload")
    log_event("Rotor Fusion: Cycle complete.")

if __name__ == "__main__":
    while True:
        run_rotor()
        time.sleep(4)
