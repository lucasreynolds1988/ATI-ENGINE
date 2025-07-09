# ~/Soap/overlay/spin_up.py

import os
import time
from core.fusion_restore_v2 import restore_from_manifest
from core.rotor_overlay import log_event
from core.cleanup_utils import clear_bloat

MANIFEST_PATH = os.path.expanduser("~/Soap/overlay/manifest.json")

def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        log_event("⚠️ No manifest.json found for spin-up.")
        return {}
    with open(MANIFEST_PATH, 'r') as f:
        return json.load(f)

def restore_files():
    manifest = load_manifest()
    if manifest:
        log_event("📦 Restoring system from manifest...")
        restore_from_manifest(manifest)
        log_event("✅ System files restored.")
    else:
        log_event("⛔ Manifest missing or empty. Skipping restore.")

def main():
    log_event("🌀 SPIN-UP triggered: Critical restoration started.")
    clear_bloat()
    restore_files()
    log_event("🧠 Warm start complete. Omega Engine entering operational state.")

if __name__ == "__main__":
    main()
