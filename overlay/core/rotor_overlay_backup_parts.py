import os
import shutil

def backup_parts(prefix, backup_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    os.makedirs(backup_dir, exist_ok=True)
    files = [f for f in os.listdir(overlay) if f.startswith(prefix) and ".part" in f]
    for f in files:
        src = os.path.join(overlay, f)
        dst = os.path.join(backup_dir, f)
        shutil.copy2(src, dst)
        print(f"Copied {f} to {backup_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        backup_parts(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_backup_parts.py <prefix> <backup_dir>")
