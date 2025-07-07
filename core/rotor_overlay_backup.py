import os
import shutil
from core.rotor_overlay import log_event

def backup_overlay(dest_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    os.makedirs(dest_dir, exist_ok=True)
    for fname in os.listdir(overlay):
        src = os.path.join(overlay, fname)
        dst = os.path.join(dest_dir, fname)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            log_event(f"rotor_overlay_backup: Backed up {fname} to {dest_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        backup_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_backup.py <backup_dir>")
