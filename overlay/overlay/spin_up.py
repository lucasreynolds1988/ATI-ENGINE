#!/usr/bin/env python3
import os, subprocess, json
from datetime import datetime
from core.fusion_restore_v2 import restore_from_manifest
from core.rotor_overlay import log_event

MANIFEST_PATH = os.path.expanduser("~/Soap/configs/critical_manifest.json")
RESTORE_PATH = os.path.expanduser("~/Soap")

def load_manifest():
    with open(MANIFEST_PATH, 'r') as f:
        return json.load(f)['critical_files']

def restore_files():
    manifest = load_manifest()
    for file_info in manifest:
        file_path = file_info['path']
        sha = file_info['sha']
        restore_from_manifest(file_path, sha, RESTORE_PATH)

def main():
    log_event("SPIN-UP", f"Critical restoration started at {datetime.utcnow().isoformat()}")
    restore_files()
    log_event("SPIN-UP", "Restoration complete. Starting Rotor Fusion.")
    subprocess.Popen(["python3", os.path.join(RESTORE_PATH, "rotor_fusion.py")])

if __name__ == "__main__":
    main()
