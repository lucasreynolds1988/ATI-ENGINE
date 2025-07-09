import os
import json
import hashlib
from core.rotor_overlay import log_event
from core.rotor_chunk_and_stream import chunk_file

BASE = os.path.expanduser("~/Soap")
MANIFEST_PATH = os.path.join(BASE, "overlay/manifest.json")
UPLOAD_DIR = os.path.join(BASE, "relay/")
CHUNK_DIR = os.path.join(BASE, "chunks/")
MAX_MB = 80
PROTECTED_DIRS = ["core", "agents", "overlay", "eyes"]

def load_manifest_paths():
    if not os.path.exists(MANIFEST_PATH):
        return []
    with open(MANIFEST_PATH, "r") as f:
        return [os.path.expanduser(entry["path"]) for entry in json.load(f)]

def sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    log_event("[CODE-RED] 🟥 Emergency offload starting...")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    total_size = 0
    protected = load_manifest_paths()

    for root, _, files in os.walk(BASE):
        for file in files:
            path = os.path.join(root, file)
            if any(p in path for p in PROTECTED_DIRS) or path in protected:
                log_event(f"[PROTECT] 🔒 {path}")
                continue

            size = os.path.getsize(path)
            total_size += size

            if size >= MAX_MB * 1024 * 1024:
                chunk_file(path, CHUNK_DIR)
                os.remove(path)
                log_event(f"[CODE-RED] 🧨 Chunked & purged: {path}")
            else:
                log_event(f"[CODE-RED] 🔹 Small file retained: {path}")

    log_event(f"[CODE-RED] ✅ Scan complete. Total scanned: {total_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
