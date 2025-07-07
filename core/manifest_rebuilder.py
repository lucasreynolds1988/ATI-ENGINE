#!/usr/bin/env python3
import os
import json
import hashlib
from core.rotor_overlay import log_event

MANIFEST_DIR = os.path.expanduser("~/Soap/overlay")
RESTORE_DIR = os.path.expanduser("~/Soap/rebuilds")
os.makedirs(RESTORE_DIR, exist_ok=True)

def sha256sum(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def rebuild_from_manifest(manifest_path):
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    out_path = os.path.join(RESTORE_DIR, manifest["original_file"])
    with open(out_path, "wb") as out:
        for part in manifest["parts"]:
            part_path = os.path.join(MANIFEST_DIR, part)
            if not os.path.exists(part_path):
                log_event(f"[REBUILD] Missing part: {part}")
                return f"❌ Missing chunk: {part}"
            with open(part_path, "rb") as p:
                out.write(p.read())
            log_event(f"[REBUILD] Appended: {part}")

    sha = sha256sum(out_path)
    if sha != manifest["sha256"]:
        log_event(f"[REBUILD] ❌ SHA Mismatch! {sha} ≠ {manifest['sha256']}")
        return "❌ Rebuild failed: SHA mismatch"

    log_event(f"[REBUILD] ✅ File rebuilt successfully: {out_path}")
    return f"✅ Rebuilt file at {out_path}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 manifest_rebuilder.py <manifest.json>")
        sys.exit(1)
    
    result = rebuild_from_manifest(sys.argv[1])
    print(result)
