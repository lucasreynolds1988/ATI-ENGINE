import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import hashlib
from core.rotor_overlay import log_event
from core.rotor_chunk_and_stream import rotor_chunk_and_upload

UPLOAD_DIR = os.path.expanduser("~/Soap/upload")
THRESHOLD = 80 * 1024 * 1024  # 80MB

def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def offload_uploads():
    total = 0
    for fname in os.listdir(UPLOAD_DIR):
        fpath = os.path.join(UPLOAD_DIR, fname)
        if os.path.isfile(fpath):
            sz = os.path.getsize(fpath)
            total += sz
            sha = sha256sum(fpath)
            log_event(f"code_red: {fname} | {sz} bytes | SHA256={sha}")
            if sz > 100 * 1024 * 1024:
                rotor_chunk_and_upload(fpath)
            else:
                os.remove(fpath)
                log_event(f"code_red: Deleted {fpath} after offload.")
    log_event(f"code_red: Upload dir processed. Total bytes={total}")

if __name__ == "__main__":
    offload_uploads()
