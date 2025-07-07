#!/usr/bin/env python3
import os, sys
import hashlib
import subprocess
import json
import threading
from core.rotor_overlay import log_event

CHUNK_SIZE = 50 * 1024 * 1024  # 50MB chunks
GCS_BUCKET = "gs://ati-oracle-engine/backups/"
UPLOAD_DIR = os.path.expanduser("~/Soap/upload")
MANIFEST_DIR = os.path.expanduser("~/Soap/overlay")

def sha256sum(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()

def chunk_file(file_path):
    part_files = []
    base = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        idx = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            partname = f"{base}.part{idx:03d}"
            partpath = os.path.join(MANIFEST_DIR, partname)
            with open(partpath, "wb") as pf:
                pf.write(chunk)
            part_files.append(partname)
            log_event(f"Chunked: {partname} ({len(chunk)} bytes)")
            idx += 1
    return part_files

def upload_part_to_gcs(partname):
    partpath = os.path.join(MANIFEST_DIR, partname)
    try:
        subprocess.run(["gsutil", "cp", partpath, GCS_BUCKET], check=True)
        log_event(f"Uploaded: {partname} to GCS")
    except Exception as e:
        log_event(f"Upload failed: {partname} | {e}")

def save_manifest(original_file, parts, full_sha):
    manifest = {
        "original_file": os.path.basename(original_file),
        "sha256": full_sha,
        "parts": parts
    }
    manifest_path = os.path.join(MANIFEST_DIR, f"{os.path.basename(original_file)}.manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    log_event(f"Saved manifest: {manifest_path}")
    return manifest_path

def rotor_chunk_and_upload(file_path):
    log_event(f"RotorChunk: Starting for {file_path}")
    full_sha = sha256sum(file_path)
    parts = chunk_file(file_path)

    threads = []
    for part in parts:
        t = threading.Thread(target=upload_part_to_gcs, args=(part,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    save_manifest(file_path, parts, full_sha)
    log_event(f"RotorChunk: Complete for {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: rotor_chunk_and_stream.py <file_path>")
        sys.exit(1)
    rotor_chunk_and_upload(sys.argv[1])
