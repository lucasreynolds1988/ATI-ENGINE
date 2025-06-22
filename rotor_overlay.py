import time
import os
from pathlib import Path

OVERLAY_DIR = Path.home() / "Soap_overlay"
DEST_DIR = Path.home() / "Soap"

def sync_overlay():
    if OVERLAY_DIR.exists():
        os.system(f"cp -r {OVERLAY_DIR}/. {DEST_DIR}")
        print("🟢 Overlay sync complete.")
    else:
        print("⚠️ Overlay directory not mounted.")

if __name__ == "__main__":
    print("🔁 [Rotor Overlay] Starting overlay loop...")
    while True:
        sync_overlay()
        time.sleep(8)
