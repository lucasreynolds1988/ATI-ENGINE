# ~/Soap/overlay/spin_down.py

import os
import shutil
import datetime
from core.rotor_overlay import log_event
from core.cleanup_utils import clear_bloat
from core.fusion_ziplog_playback import compress_and_upload_to_gcs
from core.fusion_manifest import load_manifest_paths

BACKUP_NAME = f"ATI_SPINDOWN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
BACKUP_PATH = os.path.expanduser(f"~/Soap/backups/{BACKUP_NAME}")

def spin_down():
    log_event("📉 SPIN-DOWN initiated: System backup and purge starting.")
    clear_bloat()

    protected_paths = load_manifest_paths()
    if not protected_paths:
        log_event("❌ No manifest found. Aborting to avoid data loss.")
        return

    log_event("📦 Compressing protected files...")
    os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
    compress_and_upload_to_gcs(protected_paths, BACKUP_PATH)

    log_event("🧼 Deleting unprotected files...")
    for root, dirs, files in os.walk(os.path.expanduser("~/Soap")):
        for name in files:
            file_path = os.path.join(root, name)
            if not any(file_path.startswith(p) for p in protected_paths):
                try:
                    os.remove(file_path)
                    log_event(f"🗑️ Deleted: {file_path}")
                except Exception as e:
                    log_event(f"⚠️ Delete failed: {file_path} — {e}")

    log_event("✅ SPIN-DOWN complete. Safe to power down.")

if __name__ == "__main__":
    spin_down()
