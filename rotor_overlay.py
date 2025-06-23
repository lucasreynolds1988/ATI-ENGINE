#!/usr/bin/env python3
"""
rotor_overlay.py — Synchronizes overlay files across all system areas.
Used for mirroring config, logs, or AI state snapshots across backup channels.
"""

import os
import shutil
import time
from pathlib import Path

# === Paths ===
HOME = Path.home()
BASE = HOME / "Soap"
OVERLAY = BASE / "overlay"
BACKUP = BASE / "overlay_backup"
LOG = BASE / "logs" / "overlay.log"

# === Setup ===
for d in [OVERLAY, BACKUP, LOG.parent]:
    d.mkdir(parents=True, exist_ok=True)

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] {msg}"
    print(entry)
    with open(LOG, "a") as f:
        f.write(entry + "\n")

def sync_overlay():
    log("🔄 Overlay sync started")
    synced = 0
    for file in OVERLAY.glob("*"):
        try:
            dest = BACKUP / file.name
            shutil.copy2(file, dest)
            synced += 1
            log(f"✅ Synced: {file.name}")
        except Exception as e:
            log(f"❌ Failed: {file.name} — {e}")
    log(f"🔚 Overlay sync complete — {synced} file(s) mirrored.")

if __name__ == "__main__":
    sync_overlay()
